from typing import List, Dict, Any
from content_history.models import ContentItem

class TopicExtractionService:
    """
    Derives and stores topics from historical content.
    Designed to be configurable for different AI model/provider pipelines.
    """

    def __init__(self, provider_config: Dict[str, Any] = None):
        self.config = provider_config or {}

    def extract_topics(self, item: ContentItem) -> List[str]:
        """
        Extract topics for a single item.
        If an AI provider is not available, we return a fallback or empty list,
        without fabricating complex results.
        """
        if not self.config.get("api_key"):
            # Without real AI access, fallback to basic keyword splitting if desired,
            # or just return empty indicating no topics extracted.
            # Here we do a very naive keyword extraction for demonstration of the pipeline.
            words = set(item.body.lower().split() if item.body else [])
            common = {"the", "a", "and", "or", "in", "on", "at", "to", "of", "is", "for", "with"}
            return list(words - common)[:3]

        # In a real implementation:
        # response = ai_client.generate_topics(text=item.body)
        # return response.topics
        return []

class StyleExtractionService:
    """
    Derives writing-style signals such as tone, post structure,
    opening style, CTA habits, length tendencies, etc.
    """

    def __init__(self, provider_config: Dict[str, Any] = None):
        self.config = provider_config or {}

    def extract_style_signals(self, item: ContentItem) -> Dict[str, Any]:
        """
        Analyze an item and return style signals.
        """
        body = item.body or ""
        length = len(body)

        # Simple heuristics in lieu of an AI model
        signals = {
            "length_category": "short" if length < 200 else "medium" if length < 1000 else "long",
            "has_cta": "?" in body[-100:] or "link" in body.lower() or "comment" in body.lower(),
            "formatting_tendencies": {
                "uses_lists": "\n-" in body or "\n*" in body,
                "paragraph_count": body.count("\n\n") + 1 if body else 0
            }
        }

        if self.config.get("api_key"):
            # If AI is available, we would enrich this with tone, specific structure, etc.
            pass

        return signals
