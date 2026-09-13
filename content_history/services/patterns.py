from typing import List, Dict, Any
from collections import Counter
from content_history.models import WorkspaceContentHistory
from content_history.services.extraction import TopicExtractionService, StyleExtractionService

class PatternDetectionService:
    """
    Service foundation for detecting repeated structures, recurring topics,
    and commonly used formats across a workspace's historical content.
    """

    def __init__(self, history_store: WorkspaceContentHistory):
        self.history_store = history_store
        self.topic_extractor = TopicExtractionService()
        self.style_extractor = StyleExtractionService()

    def detect_patterns(self) -> Dict[str, Any]:
        """
        Analyze the full history to detect patterns.
        """
        items = self.history_store.get_items()
        if not items:
            return {}

        all_topics = []
        lengths = []
        cta_count = 0

        for item in items:
            # Re-extract or use cached analysis_metadata
            topics = item.analysis_metadata.get("topics") or self.topic_extractor.extract_topics(item)
            style = item.analysis_metadata.get("style") or self.style_extractor.extract_style_signals(item)

            all_topics.extend(topics)
            lengths.append(style.get("length_category"))
            if style.get("has_cta"):
                cta_count += 1

        topic_counts = Counter(all_topics)
        length_counts = Counter(lengths)

        return {
            "recurring_topics": [topic for topic, count in topic_counts.most_common(5) if count > 1],
            "common_length": length_counts.most_common(1)[0][0] if length_counts else None,
            "cta_frequency": cta_count / len(items) if items else 0
        }

class PreferenceSignalService:
    """
    Extracts high-level preference signals that the Memory subsystem can ingest.
    """
    def __init__(self, pattern_service: PatternDetectionService):
        self.pattern_service = pattern_service

    def extract_preference_signals(self) -> Dict[str, Any]:
        """
        Translates raw patterns into actionable memory signals.
        """
        patterns = self.pattern_service.detect_patterns()

        signals = {
            "preferred_content_types": [],
            "frequent_topics": patterns.get("recurring_topics", []),
            "repeated_cta_behavior": "Frequent" if patterns.get("cta_frequency", 0) > 0.5 else "Occasional",
            "recurring_style_notes": []
        }

        if patterns.get("common_length"):
            signals["recurring_style_notes"].append(f"Tends to write {patterns['common_length']} posts.")

        return signals
