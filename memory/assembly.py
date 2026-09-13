from typing import Dict, Any, List
from .retrieval import RetrievalService
from .enums import MemoryCategory

class ContextAssembler:
    def __init__(self):
        self.retrieval_service = RetrievalService()

    def assemble_context(self, workspace_id: str, task_type: str, topic: str = None) -> Dict[str, Any]:
        """
        Assemble context for downstream AI consumers like Content Intelligence,
        Brainstorming, Content Map, or Agent based on task type.
        """
        context = {
            "workspace_id": workspace_id,
            "task_type": task_type,
            "memories": {}
        }

        if task_type == "brainstorming":
            context["memories"] = self._assemble_brainstorming_context(workspace_id)
        elif task_type == "content_intelligence":
            context["memories"] = self._assemble_content_intelligence_context(workspace_id, topic)
        elif task_type == "agent":
            context["memories"] = self._assemble_agent_context(workspace_id, topic)
        else:
            # Generic context
            context["memories"]["brand_rules"] = self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.BRAND_RULES.value)
            )

        return context

    def _assemble_brainstorming_context(self, workspace_id: str) -> Dict[str, List[str]]:
        return {
            "frequent_topics": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.FREQUENT_TOPICS.value)
            ),
            "unused_topics": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.UNUSED_TOPICS.value)
            ),
            "previous_topics": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.PREVIOUS_TOPICS.value)
            )
        }

    def _assemble_content_intelligence_context(self, workspace_id: str, topic: str) -> Dict[str, List[str]]:
        context = {
            "writing_style": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.WRITING_STYLE.value)
            ),
            "brand_rules": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.BRAND_RULES.value)
            ),
            "previous_mistakes": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.PREVIOUS_MISTAKES.value)
            )
        }

        if topic:
            semantic_memories = self.retrieval_service.retrieve_by_context(workspace_id, topic)
            context["topic_context"] = self._format_memories(semantic_memories)

        return context

    def _assemble_agent_context(self, workspace_id: str, topic: str) -> Dict[str, List[str]]:
        # Agent might need everything
        return {
            **self._assemble_content_intelligence_context(workspace_id, topic),
            "edit_tendencies": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.EDIT_TENDENCIES.value)
            ),
            "user_emphasis": self._format_memories(
                self.retrieval_service.retrieve_by_category(workspace_id, MemoryCategory.USER_EMPHASIS.value)
            )
        }

    def _format_memories(self, memories: List[Any]) -> List[str]:
        return [
            mem.text_value if mem.text_value else str(mem.structured_value)
            for mem in memories
        ]
