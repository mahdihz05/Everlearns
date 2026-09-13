import difflib
from typing import List, Dict, Any, Tuple
from content_history.models import ContentItem, WorkspaceContentHistory

class SimilarityService:
    """
    Foundation for detecting near-duplicate and highly similar content.
    Keep storage/retrieval integration replaceable (e.g. later swapping in vector DBs).
    """

    def __init__(self, history_store: WorkspaceContentHistory):
        self.history_store = history_store

    def check_similarity(self, new_text: str, threshold: float = 0.8) -> List[Tuple[ContentItem, float]]:
        """
        Check if the new_text is highly similar to existing items.
        Returns a list of tuples containing the similar item and the similarity score.
        This uses basic SequenceMatcher as a stand-in for vector embedding search.
        """
        if not new_text:
            return []

        similar_items = []
        for item in self.history_store.get_items():
            if not item.body:
                continue

            # Naive string similarity
            score = difflib.SequenceMatcher(None, new_text.lower(), item.body.lower()).ratio()

            if score >= threshold:
                similar_items.append((item, score))

        # Sort by highest similarity
        similar_items.sort(key=lambda x: x[1], reverse=True)
        return similar_items

    def is_duplicate(self, new_text: str) -> bool:
        """
        Quick check if an item is a near-duplicate.
        """
        matches = self.check_similarity(new_text, threshold=0.95)
        return len(matches) > 0
