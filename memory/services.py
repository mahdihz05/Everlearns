from typing import Dict, Any, Optional
from .models import WorkspaceMemory
from .vector_storage import get_embedding_provider, get_vector_storage

class MemoryService:
    def __init__(self):
        self.embedding_provider = get_embedding_provider()
        self.vector_storage = get_vector_storage()

    def upsert_memory(
        self,
        workspace_id: str,
        category: str,
        text_value: str = "",
        structured_value: Optional[Dict[str, Any]] = None,
        source: str = "",
        confidence: float = 1.0,
        supersede_existing: bool = False
    ) -> WorkspaceMemory:
        """
        Create or update a memory.
        Can come from historical content, preferences, edits, or agent interactions.
        """
        if supersede_existing:
            # Mark existing active memories in this category as inactive
            WorkspaceMemory.objects.filter(
                workspace_id=workspace_id,
                category=category,
                active=True
            ).update(active=False)

        memory = WorkspaceMemory.objects.create(
            workspace_id=workspace_id,
            category=category,
            text_value=text_value,
            structured_value=structured_value,
            source=source,
            confidence=confidence,
            active=True
        )

        # Upsert vector representation if text_value exists
        if text_value:
            vector = self.embedding_provider.get_embedding(text_value)
            self.vector_storage.upsert_vector(
                memory_id=memory.id,
                vector=vector,
                metadata={
                    "workspace_id": str(workspace_id),
                    "category": category,
                    "source": source
                }
            )

        return memory

    def supersede_memory(self, old_memory_id: int, new_memory_data: Dict[str, Any]) -> WorkspaceMemory:
        """
        Supersedes an old memory with a new one.
        """
        old_memory = WorkspaceMemory.objects.get(id=old_memory_id)
        old_memory.active = False
        old_memory.save()

        # Remove old vector from vector search to keep index clean
        self.vector_storage.delete_vector(old_memory.id)

        # Upsert the new memory
        return self.upsert_memory(
            workspace_id=old_memory.workspace_id,
            category=old_memory.category,
            **new_memory_data
        )

    def delete_memory(self, memory_id: int):
        """
        Hard delete or mark inactive based on project rules. Here we mark inactive and delete vector.
        """
        try:
            memory = WorkspaceMemory.objects.get(id=memory_id)
            memory.active = False
            memory.save()
            self.vector_storage.delete_vector(memory.id)
        except WorkspaceMemory.DoesNotExist:
            pass

    def cleanup_workspace(self, workspace_id: str):
        """
        Delete all memories for a workspace (e.g. for GDPR or workspace deletion).
        """
        WorkspaceMemory.objects.filter(workspace_id=workspace_id).delete()
        self.vector_storage.clear_workspace(str(workspace_id))

    def reindex_workspace(self, workspace_id: str):
        """
        Rebuild the vector index for a workspace from the database.
        """
        self.vector_storage.clear_workspace(str(workspace_id))

        memories = WorkspaceMemory.objects.filter(workspace_id=workspace_id, active=True)
        for memory in memories:
            if memory.text_value:
                vector = self.embedding_provider.get_embedding(memory.text_value)
                self.vector_storage.upsert_vector(
                    memory_id=memory.id,
                    vector=vector,
                    metadata={
                        "workspace_id": str(workspace_id),
                        "category": memory.category,
                        "source": memory.source
                    }
                )
