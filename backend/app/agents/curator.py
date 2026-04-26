import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json
from app.search import get_search_provider

logger = logging.getLogger("dhalee.agent.curator")

SYSTEM_PROMPT = (
    "You are The Content Curator. Your job is to find the best free learning resources for each skill gap. "
    "Use the provided search results to build a curated list. Each resource must include: skill, title, url, and a short description.\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"resources": [{"skill": "skill name", "title": "resource title", "url": "https://...", "description": "short desc"}, ...]}\n'
)


async def content_curator_node(state: DhaleeState) -> dict:
    logger.info("content_curator_node started")
    skill_gaps = state["skill_gaps"]
    provider = get_search_provider()

    all_resources = []
    for gap in skill_gaps[:6]:  # limit to top 6 gaps for POC speed
        logger.info("content_curator_node curating | gap=%s", gap)
        query = f"best free tutorial course {gap} beginner to advanced"
        search_results = await provider.search(query, max_results=3)
        search_context = "\n\n".join(
            f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}" for r in search_results
        )
        user_prompt = f"Skill Gap: {gap}\n\nSearch Results:\n{search_context}"
        result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.3)
        resources = result.get("resources", [])
        for r in resources:
            r["skill"] = gap
        all_resources.extend(resources)
        logger.info("content_curator_node gap done | gap=%s resources=%d", gap, len(resources))

    logger.info("content_curator_node finished | total_resources=%d", len(all_resources))
    return {"curated_resources": all_resources}
