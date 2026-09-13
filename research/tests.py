from django.test import TestCase
from .models import ResearchSource, ResearchJob, ResearchItem, ResearchAnalysis

class ResearchModelTests(TestCase):
    def setUp(self):
        self.source = ResearchSource.objects.create(
            workspace_id="test_ext_workspace_123",
            name="Test Source",
            platform="MANUAL"
        )
        self.job = ResearchJob.objects.create(source=self.source)
        self.item = ResearchItem.objects.create(
            job=self.job,
            source=self.source,
            original_content="Test content"
        )

    def test_models_creation(self):
        self.assertEqual(self.source.workspace_id, "test_ext_workspace_123")
        self.assertEqual(self.source.name, "Test Source")
        self.assertEqual(self.job.source, self.source)
        self.assertEqual(self.item.original_content, "Test content")

    def test_analysis_creation(self):
        analysis = ResearchAnalysis.objects.create(
            item=self.item,
            hook="Test Hook",
            tone="Professional"
        )
        self.assertEqual(analysis.hook, "Test Hook")
        self.assertEqual(analysis.tone, "Professional")
