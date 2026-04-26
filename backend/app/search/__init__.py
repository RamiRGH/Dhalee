from app.config import get_settings
from app.search.base import SearchProvider
from app.search.tavily_provider import TavilySearchProvider
from app.search.mock_provider import MockSearchProvider


_search_provider_instance: SearchProvider | None = None


def get_search_provider() -> SearchProvider:
    global _search_provider_instance
    if _search_provider_instance is not None:
        return _search_provider_instance

    settings = get_settings()
    if settings.search_provider == "tavily":
        _search_provider_instance = TavilySearchProvider()
    else:
        _search_provider_instance = MockSearchProvider()
    return _search_provider_instance
