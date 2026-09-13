from typing import List, Dict, Any, Tuple
from .retrieval import RetrievalService
from .enums import MemoryCategory

class SimilarityService:
    def __init__(self):
        self.retrieval_service = RetrievalService()

    def detect_similar_content(self, workspace_id: str, new_content: str, threshold: float = 0.85) -> List[Dict[str, Any]]:
        """
        Check if similar content has been generated before.
        In a real vector DB, we'd use cosine similarity. Here we rely on the vector storage search
        returning scores, and we filter by threshold.
        """
        # We assume RAG retrieval returns list of memories based on top-k similarity
        # With a real DB, search_vectors would return scores
        # Since our retrieval_service returns WorkspaceMemory objects, we can't easily get the score
        # unless we modify it, so let's use vector_storage directly for similarity scoring.

        provider = self.retrieval_service.embedding_provider
        storage = self.retrieval_service.vector_storage

        query_vector = provider.get_embedding(new_content)
        results = storage.search_vectors(str(workspace_id), query_vector, limit=10)

        # Filter by threshold (mock storage always returns 1.0)
        similar_items = [res for res in results if res.get("score", 0) >= threshold]
        return similar_items

    def check_previously_used_topic(self, workspace_id: str, topic: str) -> bool:
        """
        Check if a topic has been used previously.
        """
        # Could use vector similarity against PREVIOUS_TOPICS category
        similar_topics = self.retrieval_service.retrieve_by_context(
            workspace_id=workspace_id,
            topic=topic,
            category=MemoryCategory.PREVIOUS_TOPICS.value,
            limit=1
        )

    def get_undercovered_topics(self, workspace_id: str) -> List[str]:
        """
        Retrieve signals for topics not used yet or covered too little.
        """
        # Pull UNUSED_TOPICS memories directly
        unused = self.retrieval_service.retrieve_by_category(
            workspace_id,
            MemoryCategory.UNUSED_TOPICS.value
        )
        return [m.text_value for m in unused if m.text_value]
