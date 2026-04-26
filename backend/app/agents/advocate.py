import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json

logger = logging.getLogger("dhalee.agent.advocate")

SYSTEM_PROMPT = (
    "You are The Talent Advocate. Synthesize the entire user journey into a Readiness Report.\n"
    "The report should include:\n"
    "1. executive_summary: a short paragraph.\n"
    "2. skill_alignment_score: 0-100.\n"
    "3. key_strengths: list.\n"
    "4. remaining_gaps: list.\n"
    "5. recruiter_pitch: one-paragraph pitch proving the candidate is job-ready.\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"executive_summary": "...", "skill_alignment_score": 75, "key_strengths": [...], "remaining_gaps": [...], "recruiter_pitch": "..."}\n'
)


async def talent_advocate_node(state: DhaleeState) -> dict:
    logger.info("talent_advocate_node started")
    extracted_skills = state["extracted_skills"]
    skill_gaps = state["skill_gaps"]
    market_requirements = state["market_requirements"]
    learning_roadmap = state["learning_roadmap"]
    coach_feedback = state["coach_feedback"]

    user_prompt = (
        f"Extracted Skills: {', '.join(extracted_skills)}\n\n"
        f"Skill Gaps: {', '.join(skill_gaps)}\n\n"
        f"Market Requirements: {', '.join(market_requirements)}\n\n"
        f"Coach Feedback: {coach_feedback}\n\n"
        f"Roadmap Weeks: {len(learning_roadmap.get('weeks', []))}\n\n"
        "Generate the final Readiness Report."
    )
    result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.3)

    logger.info(
        "talent_advocate_node finished | score=%s | strengths=%d | gaps=%d",
        result.get("skill_alignment_score"),
        len(result.get("key_strengths", [])),
        len(result.get("remaining_gaps", [])),
    )

    return {"readiness_report": result}
