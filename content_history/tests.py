import unittest
from content_history.models import WorkspaceContentHistory, ContentItem, Platform
from content_history.services.similarity import SimilarityService
from content_history.connectors.telegram import TelegramConnector

class TestContentHistory(unittest.TestCase):

    def setUp(self):
        self.workspace_id = "ws_123"
        self.history = WorkspaceContentHistory(self.workspace_id)

    def test_add_item_idempotency(self):
        item1 = ContentItem(
            workspace_id=self.workspace_id,
            platform=Platform.TELEGRAM,
            external_id="msg_1",
            body="Hello World"
        )
        # Should be new
        self.assertTrue(self.history.add_item(item1))

        # Should be duplicate
        item2 = ContentItem(
            workspace_id=self.workspace_id,
            platform=Platform.TELEGRAM,
            external_id="msg_1",
            body="Hello World Updated"
        )
        self.assertFalse(self.history.add_item(item2))

        # Total should remain 1
        self.assertEqual(len(self.history.get_items()), 1)

    def test_similarity_service(self):
        item1 = ContentItem(
            workspace_id=self.workspace_id,
            platform=Platform.TELEGRAM,
            external_id="msg_1",
            body="This is a test message for similarity."
        )
        self.history.add_item(item1)

        sim_service = SimilarityService(self.history)

        # Exact match
        self.assertTrue(sim_service.is_duplicate("This is a test message for similarity."))

        # Near match
        self.assertTrue(sim_service.is_duplicate("This is a test message for similarity!"))

        # Completely different
        self.assertFalse(sim_service.is_duplicate("Something entirely different."))

    def test_connector_configuration(self):
        connector = TelegramConnector()
        self.assertFalse(connector.is_configured())

        connector.configure({"bot_token": "token", "chat_id": "id"})
        self.assertTrue(connector.is_configured())

if __name__ == '__main__':
    unittest.main()
