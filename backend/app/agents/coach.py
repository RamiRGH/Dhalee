import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json

logger = logging.getLogger("dhalee.agent.coach")

SYSTEM_PROMPT = (
    "You are The Performance Coach. Review the learning roadmap and provide feedback.\n"
    "Check for: unrealistic timelines, missing prerequisites, poor sequencing, or gaps in coverage.\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"feedback": "short paragraph of critique", "needs_revision": true/false}\n'
)


async def performance_coach_node(state: DhaleeState) -> dict:
    logger.info("performance_coach_node started")
    roadmap = state["learning_roadmap"]
    skill_gaps = state["skill_gaps"]

    user_prompt = (
        f"Skill Gaps: {', '.join(skill_gaps)}\n\n"
        f"Roadmap:\n{str(roadmap)[:6000]}\n\n"
        "Provide your coaching feedback."
    )
    result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.3)

    feedback = result.get("feedback", "")
    logger.info("performance_coach_node finished | feedback_len=%d", len(feedback))

    return {
        "coach_feedback": feedback,
    }
