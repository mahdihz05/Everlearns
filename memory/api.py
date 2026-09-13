from typing import Dict, Any, List, Optional
from .services import MemoryService
from .retrieval import RetrievalService
from .assembly import ContextAssembler
from .similarity import SimilarityService
from .models import WorkspaceMemory

class MemoryAPI:
    """
    Facade for downstream modules (Content Intelligence, Agent, etc) to interact with Memory.
    Ensures safe, cross-workspace isolated access.
    """
    def __init__(self):
        self.memory_service = MemoryService()
        self.retrieval_service = RetrievalService()
        self.assembler = ContextAssembler()
        self.similarity_service = SimilarityService()

    # --- UPSERT ---
    def add_memory(self, workspace_id: str, category: str, text_value: str = "", **kwargs) -> WorkspaceMemory:
        return self.memory_service.upsert_memory(workspace_id, category, text_value, **kwargs)

    # --- RETRIEVAL & ASSEMBLY ---
    def get_context_for_task(self, workspace_id: str, task_type: str, topic: Optional[str] = None) -> Dict[str, Any]:
        return self.assembler.assemble_context(workspace_id, task_type, topic)

    def retrieve_topic_context(self, workspace_id: str, topic: str, limit: int = 5) -> List[WorkspaceMemory]:
        return self.retrieval_service.retrieve_by_context(workspace_id, topic, limit=limit)

    # --- SIMILARITY & GAPS ---
    def is_similar_to_existing(self, workspace_id: str, text: str, threshold: float = 0.85) -> bool:
        matches = self.similarity_service.detect_similar_content(workspace_id, text, threshold)
        return len(matches) > 0

    def get_unused_topics(self, workspace_id: str) -> List[str]:
        return self.similarity_service.get_undercovered_topics(workspace_id)

    # --- LIFECYCLE ---
    def delete_workspace_memory(self, workspace_id: str):
        self.memory_service.cleanup_workspace(workspace_id)
