from django.test import TestCase
from .models import ContentPattern, PatternEvidence
from research.models import ResearchSource, ResearchJob, ResearchItem, ResearchAnalysis
from .services import extract_candidate_patterns, promote_pattern, deprecate_pattern

class PatternTests(TestCase):
    def setUp(self):
        self.source = ResearchSource.objects.create(workspace_id="test_workspace_999", name="Src", platform="MANUAL")
        self.job = ResearchJob.objects.create(source=self.source)
        self.item = ResearchItem.objects.create(job=self.job, source=self.source, original_content="Content")
        self.analysis = ResearchAnalysis.objects.create(item=self.item, hook="Catchy hook")

    def test_pattern_extraction_service(self):
        candidates = extract_candidate_patterns(self.analysis)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].description, "Catchy hook")
        self.assertEqual(candidates[0].status, "CANDIDATE")

        # Test promotion
        promoted = promote_pattern(candidates[0])
        self.assertTrue(promoted)
        self.assertEqual(candidates[0].status, "APPROVED")

        # Test deprecation
        deprecate_pattern(candidates[0])
        self.assertEqual(candidates[0].status, "DEPRECATED")
