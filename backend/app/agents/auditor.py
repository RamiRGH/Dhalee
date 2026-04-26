import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json

logger = logging.getLogger("dhalee.agent.auditor")

SYSTEM_PROMPT = (
    "You are The Skill Auditor. Your job is to deeply analyze a CV and extract:\n"
    "1. A list of explicit and inferred technical and soft skills.\n"
    "2. A list of skill gaps compared to the desired role.\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"extracted_skills": ["skill1", "skill2", ...], "skill_gaps": ["gap1", "gap2", ...]}\n'
    "Be thorough but concise."
)


async def skill_auditor_node(state: DhaleeState) -> dict:
    logger.info("skill_auditor_node started")
    cv_text = state["cv_text"]
    desired_role = state["desired_role"]

    user_prompt = f"Desired Role: {desired_role}\n\nCV Text:\n{cv_text[:8000]}"
    result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.2)

    extracted = result.get("extracted_skills", [])
    gaps = result.get("skill_gaps", [])
    logger.info("skill_auditor_node finished | extracted=%d gaps=%d", len(extracted), len(gaps))

    return {
        "extracted_skills": extracted,
        "skill_gaps": gaps,
    }
