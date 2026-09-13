from typing import List, Dict, Any, Optional
from .adapters import ContentHistoryAdapter, WorkspaceMemoryAdapter, ContentPatternLibraryAdapter
from .search import WebSearchProvider

class BrainstormingService:
    def __init__(
        self,
        history_adapter: ContentHistoryAdapter,
        memory_adapter: WorkspaceMemoryAdapter,
        pattern_adapter: ContentPatternLibraryAdapter,
        search_provider: WebSearchProvider
    ):
        self.history = history_adapter
        self.memory = memory_adapter
        self.patterns = pattern_adapter
        self.search = search_provider

    def generate_topic_suggestions(self, workspace_id: int) -> List[Dict[str, str]]:
        # 1. Fetch memory core themes
        themes = self.memory.get_core_themes(workspace_id)

        # 2. Check history to avoid duplication
        covered = self.history.get_topics_covered(workspace_id)

        # 3. Get trends if available
        trends = []
        for theme in themes:
            trends.extend(self.search.get_trends(theme))

        # Mock logic to combine these into new suggestions
        suggestions = []
        for theme in themes:
            if theme not in covered:
                suggestions.append({"topic": f"Deep dive into {theme}", "reason": "Core theme not recently covered"})

        if trends:
            suggestions.append({"topic": trends[0], "reason": "Current trend related to your themes"})

        return suggestions

    def generate_angles(self, topic: str, workspace_id: int) -> List[Dict[str, str]]:
        # Fetch memory context to tailor the angles
        context = self.memory.query_memory(workspace_id, f"Context for {topic}")

        # Mock generation of angles
        return [
            {"angle": "Beginner's Guide", "audience": "Newcomers"},
            {"angle": "Advanced Techniques", "audience": "Professionals"},
            {"angle": "Case Study", "audience": "Decision Makers"}
        ]

    def generate_alternatives(self, idea_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Mock generation of alternative paths for a rough idea
        return [
            {**idea_data, "suggested_platform": "Twitter", "suggested_content_type": "Thread"},
            {**idea_data, "suggested_platform": "LinkedIn", "suggested_content_type": "Long-form Post"},
            {**idea_data, "suggested_platform": "YouTube", "suggested_content_type": "Short Video"}
        ]
