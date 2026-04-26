from typing import List, Dict
from app.search.base import SearchProvider


class MockSearchProvider(SearchProvider):
    """
    Offline mock search provider for testing without API keys.
    Returns generic but plausible resource placeholders.
    """

    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        return [
            {
                "title": f"Top guide for: {query}",
                "url": "https://example.com/resource",
                "content": "A comprehensive guide covering fundamentals to advanced topics.",
            },
            {
                "title": f"YouTube tutorial on {query}",
                "url": "https://youtube.com/example",
                "content": "Step-by-step video tutorial with practical examples.",
            },
            {
                "title": f"Coursera course for {query}",
                "url": "https://coursera.org/example",
                "content": "University-level course with hands-on projects and certification.",
            },
        ]
