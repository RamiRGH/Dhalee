import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json

logger = logging.getLogger("dhalee.agent.architect")

SYSTEM_PROMPT = (
    "You are The Roadmap Architect. Your job is to design a structured, week-by-week learning journey.\n"
    "Given the skill gaps and curated resources, build a realistic 4-to-8 week roadmap.\n"
    "Each week should have: week_number, focus_skills, objectives, and resources_to_use (list of titles/urls).\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"roadmap": {"weeks": [{"week_number": 1, "focus_skills": ["..."], "objectives": ["..."], "resources_to_use": [{"title": "...", "url": "..."}]}, ...]}}\n'
)


async def roadmap_architect_node(state: DhaleeState) -> dict:
    logger.info("roadmap_architect_node started")
    skill_gaps = state["skill_gaps"]
    resources = state["curated_resources"]

    resources_text = "\n".join(
        f"- {r['skill']}: {r['title']} ({r['url']})" for r in resources
    )

    user_prompt = (
        f"Skill Gaps: {', '.join(skill_gaps)}\n\n"
        f"Curated Resources:\n{resources_text}\n\n"
        "Design a week-by-week learning roadmap."
    )
    logger.info("roadmap_architect_node calling LLM | gaps=%d resources=%d", len(skill_gaps), len(resources))
    result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.3)

    roadmap = result.get("roadmap", {})
    weeks = roadmap.get("weeks", [])
    logger.info("roadmap_architect_node finished | weeks=%d", len(weeks))

    return {"learning_roadmap": roadmap}
