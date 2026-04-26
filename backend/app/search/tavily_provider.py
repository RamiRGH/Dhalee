from typing import List, Dict
from tavily import TavilyClient
from app.search.base import SearchProvider
from app.config import get_settings


class TavilySearchProvider(SearchProvider):
    def __init__(self):
        settings = get_settings()
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        response = self.client.search(query=query, max_results=max_results, search_depth="basic")
        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
            })
        return results
