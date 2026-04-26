import logging
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json

from app.cv_parser.parser import parse_cv
from app.cv_parser.validator import validate_cv_is_ats_compatible
from app.agents.graph import build_graph
from app.schemas import DhaleeState

# Configure logging early
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("dhalee.api")

app = FastAPI(title="Dhalee POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def stream_analysis(cv_text: str, desired_role: str):
    graph = build_graph()

    initial_state: DhaleeState = {
        "cv_text": cv_text,
        "desired_role": desired_role,
        "extracted_skills": [],
        "skill_gaps": [],
        "market_requirements": [],
        "curated_resources": [],
        "learning_roadmap": {},
        "coach_feedback": "",
        "readiness_report": {},
        "error": None,
    }

    agent_display_names = {
        "skill_auditor": "Skill Auditor",
        "market_scout": "Market Scout",
        "content_curator": "Content Curator",
        "roadmap_architect": "Roadmap Architect",
        "performance_coach": "Performance Coach",
        "talent_advocate": "Talent Advocate",
    }

    logger.info("Starting stream_analysis for desired_role=%s", desired_role)
    yield json.dumps({"type": "progress", "agent": "start", "message": "Starting analysis..."}) + "\n"

    current_state: DhaleeState = dict(initial_state)  # shallow copy to accumulate updates

    try:
        step_count = 0
        async for event in graph.astream(initial_state):
            step_count += 1
            logger.debug("LangGraph event #%d keys=%s", step_count, list(event.keys()))
            for node_name, update in event.items():
                # Merge partial updates into accumulated state
                if isinstance(update, dict):
                    current_state.update(update)

                if node_name in agent_display_names:
                    logger.info("Agent completed: %s", node_name)
                    yield json.dumps({
                        "type": "progress",
                        "agent": node_name,
                        "message": f"{agent_display_names[node_name]} is working...",
                    }) + "\n"
        logger.info("LangGraph stream finished after %d events", step_count)
    except Exception as e:
        logger.exception("LangGraph stream failed")
        yield json.dumps({"type": "error", "message": str(e)}) + "\n"
        return

    logger.info(
        "Returning final state | skills=%d gaps=%d reqs=%d resources=%d roadmap_weeks=%d report_keys=%s",
        len(current_state.get("extracted_skills", [])),
        len(current_state.get("skill_gaps", [])),
        len(current_state.get("market_requirements", [])),
        len(current_state.get("curated_resources", [])),
        len(current_state.get("learning_roadmap", {}).get("weeks", [])),
        list(current_state.get("readiness_report", {}).keys()),
    )

    yield json.dumps({
        "type": "complete",
        "data": {
            "extracted_skills": current_state.get("extracted_skills", []),
            "skill_gaps": current_state.get("skill_gaps", []),
            "market_requirements": current_state.get("market_requirements", []),
            "curated_resources": current_state.get("curated_resources", []),
            "learning_roadmap": current_state.get("learning_roadmap", {}),
            "coach_feedback": current_state.get("coach_feedback", ""),
            "readiness_report": current_state.get("readiness_report", {}),
        },
    }) + "\n"


@app.post("/api/analyze")
async def analyze(
    cv_file: UploadFile = File(...),
    desired_role: str = Form(...),
):
    logger.info("Received analyze request | filename=%s desired_role=%s", cv_file.filename, desired_role)

    if not desired_role or not desired_role.strip():
        logger.warning("Rejecting request: empty desired_role")
        raise HTTPException(status_code=400, detail="Desired role is required.")

    filename = cv_file.filename or ""
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
        logger.warning("Rejecting request: unsupported file type | filename=%s", filename)
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_bytes = await cv_file.read()
    if len(file_bytes) == 0:
        logger.warning("Rejecting request: empty file")
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    logger.info("File read OK | bytes=%d", len(file_bytes))

    try:
        cv_text = parse_cv(file_bytes, filename)
        logger.info("CV parsed OK | chars=%d", len(cv_text))
    except Exception as e:
        logger.exception("CV parse failed")
        raise HTTPException(status_code=400, detail=f"Failed to parse CV: {str(e)}")

    if len(cv_text.strip()) < 50:
        logger.warning("CV text too short after parsing | chars=%d", len(cv_text.strip()))
        raise HTTPException(
            status_code=400,
            detail="Your file does not appear to be a CV or is not ATS compatible. Parsed text is too short."
        )

    logger.info("Running ATS validation...")
    is_cv, reason = await validate_cv_is_ats_compatible(cv_text)
    if not is_cv:
        logger.warning("ATS validation failed | reason=%s", reason)
        raise HTTPException(
            status_code=400,
            detail=f"Your file does not appear to be a CV or is not ATS compatible. Reason: {reason}"
        )
    logger.info("ATS validation passed")

    return StreamingResponse(
        stream_analysis(cv_text, desired_role.strip()),
        media_type="text/event-stream",
    )


@app.get("/api/health")
async def health():
    return {"status": "ok"}
