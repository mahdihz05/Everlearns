from django.test import TestCase
from .api import MemoryAPI
from .enums import MemoryCategory
from .models import WorkspaceMemory
import uuid

class MemorySystemTests(TestCase):
    def setUp(self):
        self.api = MemoryAPI()
        self.workspace_id = str(uuid.uuid4())
        self.workspace_id_2 = str(uuid.uuid4())

    def test_upsert_and_retrieve(self):
        # Create a memory
        mem = self.api.add_memory(
            self.workspace_id,
            MemoryCategory.WRITING_STYLE.value,
            text_value="Use active voice."
        )
        self.assertEqual(mem.category, MemoryCategory.WRITING_STYLE.value)
        self.assertTrue(mem.active)

        # Retrieve by category (using internal service directly for test validation)
        retrieved = self.api.retrieval_service.retrieve_by_category(self.workspace_id, MemoryCategory.WRITING_STYLE.value)
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0].text_value, "Use active voice.")

    def test_workspace_isolation(self):
        self.api.add_memory(self.workspace_id, MemoryCategory.BRAND_RULES.value, text_value="No emojis.")

        # Workspace 2 should not see workspace 1's memory
        retrieved = self.api.retrieval_service.retrieve_by_category(self.workspace_id_2, MemoryCategory.BRAND_RULES.value)
        self.assertEqual(len(retrieved), 0)

    def test_context_assembly(self):
        self.api.add_memory(self.workspace_id, MemoryCategory.WRITING_STYLE.value, text_value="Casual tone.")
        self.api.add_memory(self.workspace_id, MemoryCategory.BRAND_RULES.value, text_value="Company name is EverLearns.")

        context = self.api.get_context_for_task(self.workspace_id, task_type="content_intelligence", topic="AI")
        self.assertIn("writing_style", context["memories"])
        self.assertEqual(context["memories"]["writing_style"], ["Casual tone."])
        self.assertEqual(context["memories"]["brand_rules"], ["Company name is EverLearns."])

    def test_supersede_memory(self):
        mem1 = self.api.add_memory(self.workspace_id, MemoryCategory.CTA_PREFERENCES.value, text_value="Click here")
        self.api.memory_service.supersede_memory(mem1.id, {"text_value": "Learn more"})

        # Old memory should be inactive
        mem1.refresh_from_db()
        self.assertFalse(mem1.active)

        # Should have exactly 1 active memory
        active_mems = self.api.retrieval_service.retrieve_by_category(self.workspace_id, MemoryCategory.CTA_PREFERENCES.value)
        self.assertEqual(len(active_mems), 1)
        self.assertEqual(active_mems[0].text_value, "Learn more")
