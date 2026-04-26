import logging
from app.schemas import DhaleeState
from app.agents.llm_utils import llm_json
from app.search import get_search_provider

logger = logging.getLogger("dhalee.agent.scout")

SYSTEM_PROMPT = (
    "You are The Market Scout. Your job is to research what the Saudi job market and Vision 2030 "
    "industries require for a given role. Synthesize the search results into a concise list of "
    "key market requirements, technologies, certifications, and trends.\n"
    "Respond ONLY with JSON in this exact format:\n"
    '{"market_requirements": ["req1", "req2", ...]}\n'
)


async def market_scout_node(state: DhaleeState) -> dict:
    logger.info("market_scout_node started")
    desired_role = state["desired_role"]
    provider = get_search_provider()

    query = f"Saudi Arabia Vision 2030 {desired_role} job requirements skills 2024 2025"
    logger.info("market_scout_node searching | query=%s", query)
    search_results = await provider.search(query, max_results=5)
    logger.info("market_scout_node search returned | results=%d", len(search_results))

    search_context = "\n\n".join(
        f"Title: {r['title']}\nContent: {r['content']}" for r in search_results
    )

    user_prompt = f"Desired Role: {desired_role}\n\nSearch Results:\n{search_context}"
    result = await llm_json(SYSTEM_PROMPT, user_prompt, temperature=0.3)

    reqs = result.get("market_requirements", [])
    logger.info("market_scout_node finished | requirements=%d", len(reqs))
    return {
        "market_requirements": reqs,
    }
