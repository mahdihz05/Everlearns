from typing import List, Dict, Any, Optional

class WebSearchProvider:
    """Abstraction for web search capabilities."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.is_available = bool(api_key)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        if not self.is_available:
            # Fallback behavior when web search is unavailable
            print("Web search is currently unavailable. Returning mock/empty results.")
            return []

        # Implementation for actual web search would go here
        # Return format: [{"title": "...", "snippet": "...", "link": "..."}]
        return [
            {"title": f"Result for {query}", "snippet": "Sample snippet", "link": "http://example.com"}
        ]

    def get_trends(self, topic: str) -> List[str]:
        if not self.is_available:
            print("Web search is currently unavailable. Cannot fetch live trends.")
            return []

        return [f"Trend 1 for {topic}", f"Trend 2 for {topic}"]
