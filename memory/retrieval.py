from typing import List, Dict, Any, Optional
from .models import WorkspaceMemory
from .vector_storage import get_embedding_provider, get_vector_storage

class RetrievalService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()
        self.vector_storage = get_vector_storage()

    def retrieve_by_context(
        self,
        workspace_id: str,
        topic: str,
        category: Optional[str] = None,
        metadata_filters: Optional[Dict[str, Any]] = None,
        limit: int = 5
    ) -> List[WorkspaceMemory]:
        """
        Retrieves relevant memories for a workspace by topic/context.
        Cross-workspace retrieval is strictly prevented by enforcing workspace_id.
        """
        if not workspace_id:
            raise ValueError("workspace_id is required to prevent cross-workspace retrieval")

        # Get query embedding
        query_vector = self.embedding_provider.get_embedding(topic)

        # Search vector storage
        search_results = self.vector_storage.search_vectors(
            workspace_id=str(workspace_id),
            query_vector=query_vector,
            category=category,
            limit=limit
        )

        memory_ids = [result["memory_id"] for result in search_results]

        # Fetch from DB
        queryset = WorkspaceMemory.objects.filter(
            id__in=memory_ids,
            workspace_id=workspace_id,
            active=True
        )

        # Apply metadata filters if any (e.g. source, recency/priority)
        if metadata_filters:
            if 'source' in metadata_filters:
                queryset = queryset.filter(source=metadata_filters['source'])
            if 'min_confidence' in metadata_filters:
                queryset = queryset.filter(confidence__gte=metadata_filters['min_confidence'])

        # Order by recency (or could be priority if confidence was used)
        queryset = queryset.order_by('-created_at')

        return list(queryset)

    def retrieve_by_category(self, workspace_id: str, category: str, limit: int = 10) -> List[WorkspaceMemory]:
        """
        Directly retrieve active memories by category for a specific workspace.
        """
        if not workspace_id:
            raise ValueError("workspace_id is required to prevent cross-workspace retrieval")

        return list(
            WorkspaceMemory.objects.filter(
                workspace_id=workspace_id,
                category=category,
                active=True
            ).order_by('-created_at')[:limit]
        )
