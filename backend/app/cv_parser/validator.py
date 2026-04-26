import logging
from app.agents.llm_utils import llm_json

logger = logging.getLogger("dhalee.cv_validator")


async def validate_cv_is_ats_compatible(cv_text: str) -> tuple[bool, str]:
    """
    Uses an LLM to check if the parsed text is representative of a CV.
    Returns (is_valid, reason).
    """
    logger.info("ATS validation started | text_len=%d", len(cv_text))

    system_prompt = (
        "You are an ATS (Applicant Tracking System) compatibility checker. "
        "Analyze the following text and determine if it is a valid, parseable CV/resume. "
        "Look for typical CV sections such as: contact info, summary/objective, work experience, "
        "education, skills, certifications, projects, etc. "
        "Respond ONLY with a JSON object in this exact format:\n"
        '{"is_cv": true/false, "reason": "short explanation"}\n'
        "Do not include markdown code fences or any extra text."
    )

    result = await llm_json(system_prompt, cv_text[:8000], temperature=0.0)
    is_cv = result.get("is_cv", False)
    reason = result.get("reason", "No reason provided.")
    logger.info("ATS validation result | is_cv=%s reason=%s", is_cv, reason)
    return is_cv, reason
