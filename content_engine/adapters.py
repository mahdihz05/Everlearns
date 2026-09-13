from typing import List, Dict, Any, Optional

class PatternLibraryAdapter:
    """
    Adapter to retrieve relevant content patterns.
    """
    def get_patterns(
        self,
        platform: Optional[str] = None,
        content_type: Optional[str] = None,
        goal: Optional[str] = None,
        topic: Optional[str] = None,
        tone: Optional[str] = None
    ) -> Dict[str, Any]:
        # Graceful absence: return empty dict if not available
        return {}


class ContentHistoryAdapter:
    """
    Adapter to retrieve content history context.
    """
    def get_recent_content(self, workspace_id: str, topic: str) -> List[str]:
        # Graceful absence
        return []

    def get_similar_content(self, topic: str) -> List[str]:
        # Graceful absence
        return []


class MemoryAdapter:
    """
    Adapter to retrieve workspace memory rules.
    """
    def get_workspace_rules(self, workspace_id: str) -> Dict[str, Any]:
        # Return default/empty if unavailable
        return {
            "preferred_tone": None,
            "brand_rules": [],
            "style": None,
            "cta_preferences": [],
            "known_mistakes": [],
            "under_covered_topics": []
        }
