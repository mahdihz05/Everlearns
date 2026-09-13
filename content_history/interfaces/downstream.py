from typing import List, Dict, Any
from content_history.models import WorkspaceContentHistory
from content_history.services.similarity import SimilarityService
from content_history.services.patterns import PreferenceSignalService, PatternDetectionService

class ContentHistoryAdapter:
    """
    Exposes clean interfaces for downstream systems to consume historical content.
    """

    def __init__(self, history_store: WorkspaceContentHistory):
        self.history_store = history_store

    def get_memory_rag_context(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Provides context for Memory/RAG ingestion.
        Returns the most relevant/recent items structured for embedding.
        """
        items = sorted(
            self.history_store.get_items(),
            key=lambda x: x.created_at,
            reverse=True
        )[:limit]

        return [
            {
                "public_id": item.public_id,
                "text": item.body,
                "metadata": {
                    "platform": item.platform.value,
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                    "topics": item.analysis_metadata.get("topics", [])
                }
            }
            for item in items if item.body
        ]

    def get_content_intelligence_context(self) -> Dict[str, Any]:
        """
        Provides context for Content Intelligence (patterns, signals).
        """
        pattern_service = PatternDetectionService(self.history_store)
        pref_service = PreferenceSignalService(pattern_service)

        return {
            "preferences": pref_service.extract_preference_signals(),
            "patterns": pattern_service.detect_patterns()
        }

    def get_brainstorming_context(self, limit: int = 10) -> List[str]:
        """
        Provides recent successful topics/posts as inspiration for Brainstorming.
        """
        items = sorted(
            self.history_store.get_items(),
            key=lambda x: x.created_at,
            reverse=True
        )[:limit]

        return [item.title for item in items if item.title]

    def check_duplicate_topic(self, new_text: str) -> bool:
        """
        Adapter for checking if a proposed topic/content is a near-duplicate.
        """
        sim_service = SimilarityService(self.history_store)
        return sim_service.is_duplicate(new_text)

    def get_content_map_analysis(self) -> Dict[str, Any]:
        """
        Provides a mapping of topics to frequency and timeline.
        """
        items = self.history_store.get_items()
        topic_timeline = []

        for item in items:
            topics = item.analysis_metadata.get("topics", [])
            if topics:
                topic_timeline.append({
                    "date": item.created_at.isoformat() if item.created_at else None,
                    "topics": topics
                })

        return {
            "total_analyzed": len(items),
            "timeline": topic_timeline
        }
