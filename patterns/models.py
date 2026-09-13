import uuid
from django.db import models
from research.models import ResearchItem

class PatternCategory(models.TextChoices):
    STRUCTURE = 'STRUCTURE', 'Structure'
    HOOK = 'HOOK', 'Hook'
    TONE = 'TONE', 'Tone'
    CTA = 'CTA', 'Call to Action'
    VISUAL = 'VISUAL', 'Visual'
    SIMPLIFICATION = 'SIMPLIFICATION', 'Concept Simplification'
    OTHER = 'OTHER', 'Other'

class PatternStatus(models.TextChoices):
    CANDIDATE = 'CANDIDATE', 'Candidate'
    APPROVED = 'APPROVED', 'Approved (Library Entry)'
    DEPRECATED = 'DEPRECATED', 'Deprecated'

class ContentPattern(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=PatternCategory.choices, default=PatternCategory.OTHER)
    status = models.CharField(max_length=50, choices=PatternStatus.choices, default=PatternStatus.CANDIDATE)

    # Applicability
    applicable_platforms = models.JSONField(default=list, blank=True, help_text="List of applicable platforms")
    applicable_content_categories = models.JSONField(default=list, blank=True, help_text="List of applicable content categories")

    tags = models.JSONField(default=list, blank=True, help_text="List of tags/topics")
    structured_attributes = models.JSONField(default=dict, blank=True)
    ai_consumable_representation = models.JSONField(default=dict, blank=True, help_text="Normalized format for AI use")

    quality_confidence = models.FloatField(default=0.0, help_text="0.0 to 1.0 confidence score")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

class PatternEvidence(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pattern = models.ForeignKey(ContentPattern, on_delete=models.CASCADE, related_name='evidence')
    research_item = models.ForeignKey(ResearchItem, on_delete=models.CASCADE, related_name='pattern_evidence')
    relevance_score = models.FloatField(default=1.0)
    extraction_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pattern', 'research_item')

    def __str__(self):
        return f"Evidence for {self.pattern.name} from Item {self.research_item.id}"
