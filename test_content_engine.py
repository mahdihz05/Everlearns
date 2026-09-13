import sys
import unittest
from content_engine.models import GenerationRequest
from content_engine.operations import ContentEngine
from content_engine.providers import DummyAIProvider
from content_engine.platforms import get_platform_strategy
from content_engine.prompts import compose_prompt

class TestContentEngine(unittest.TestCase):
    def setUp(self):
        self.provider = DummyAIProvider()
        self.engine = ContentEngine(self.provider)

    def test_generation_request_model(self):
        req = GenerationRequest(topic="Test Topic", platform="Telegram")
        self.assertEqual(req.topic, "Test Topic")
        self.assertEqual(req.platform, "Telegram")
        self.assertEqual(req.output_language, "en")

    def test_platform_strategy(self):
        strategy = get_platform_strategy("Telegram")
        rules = strategy.get_platform_rules()
        self.assertIn("length", rules)
        self.assertEqual(rules["length"], "short-to-medium")

        # Test fallback
        strategy = get_platform_strategy("UnknownPlatform")
        rules = strategy.get_platform_rules()
        self.assertEqual(rules["length"], "medium")

    def test_prompt_composition(self):
        context = {"topic": "AI Engineering", "platform": "LinkedIn"}
        prompt_text, version = compose_prompt("system_default", context)
        self.assertIn("AI Engineering", prompt_text)
        self.assertIn("LinkedIn", prompt_text)

    def test_generate_content(self):
        req = GenerationRequest(topic="AI", platform="LinkedIn", workspace_id="ws-123")
        res = self.engine.generate_content(req)
        self.assertTrue(res.generated_text.startswith("Dummy generated content for prompt"))
        self.assertEqual(res.provider, "dummy")
        self.assertEqual(res.model, "dummy-model")

        # Context should include platform rules
        self.assertIn("additional_instructions", res.source_context)
        self.assertIn("medium-to-long", res.source_context["additional_instructions"])

    def test_generate_hashtags(self):
        req = GenerationRequest(topic="Space")
        res = self.engine.generate_hashtags(req)
        # Dummy provider just returns text starting with "Dummy generated content..."
        # The hashtag generator should prefix each word with #
        self.assertTrue(all(h.startswith("#") for h in res.hashtags))

    def test_rewrite_text(self):
        req = GenerationRequest(topic="Rewrite")
        res = self.engine.rewrite_text("Original text here", req)
        self.assertIn("additional_instructions", res.source_context)
        self.assertIn("Rewrite the following text", res.source_context["additional_instructions"])

if __name__ == "__main__":
    unittest.main()
