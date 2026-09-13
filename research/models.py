import uuid
from django.db import models

class SourcePlatform(models.TextChoices):
    TELEGRAM_CHANNEL = 'TELEGRAM_CHANNEL', 'Telegram Channel'
    TELEGRAM_GROUP = 'TELEGRAM_GROUP', 'Telegram Group'
    LINKEDIN = 'LINKEDIN', 'LinkedIn'
    WORDPRESS = 'WORDPRESS', 'WordPress'
    MANUAL = 'MANUAL', 'Manual/Dataset'

class ResearchSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace_id = models.CharField(max_length=255, help_text="Reference to external Workspace subsystem")
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=50, choices=SourcePlatform.choices)
    source_url = models.URLField(max_length=1000, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.platform})"

class ProcessingState(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'

class ResearchJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source = models.ForeignKey(ResearchSource, on_delete=models.CASCADE, related_name='jobs')
    state = models.CharField(max_length=50, choices=ProcessingState.choices, default=ProcessingState.PENDING)
    error_metadata = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Job {self.id} for {self.source.name} - {self.state}"

class AnalysisState(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ANALYZED = 'ANALYZED', 'Analyzed'
    FAILED = 'FAILED', 'Failed'

class ResearchItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(ResearchJob, on_delete=models.CASCADE, related_name='items')
    source = models.ForeignKey(ResearchSource, on_delete=models.CASCADE, related_name='items')
    original_content = models.TextField()
    reference_url = models.URLField(max_length=1000, blank=True, null=True)
    analysis_state = models.CharField(max_length=50, choices=AnalysisState.choices, default=AnalysisState.PENDING)
    external_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID from the source platform")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.id} from {self.source.name}"

class ResearchAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.OneToOneField(ResearchItem, on_delete=models.CASCADE, related_name='analysis')

    # Analysis Dimensions
    hook = models.TextField(blank=True, null=True)
    tone = models.CharField(max_length=100, blank=True, null=True)
    length_class = models.CharField(max_length=50, blank=True, null=True)
    headline_pattern = models.CharField(max_length=255, blank=True, null=True)
    section_structure = models.JSONField(default=list, blank=True, help_text="List of structural elements")
    cta_pattern = models.CharField(max_length=255, blank=True, null=True)
    content_angle = models.CharField(max_length=255, blank=True, null=True)
    concept_simplification_pattern = models.TextField(blank=True, null=True)
    serialization_pattern = models.CharField(max_length=255, blank=True, null=True)
    visual_strategy = models.CharField(max_length=255, blank=True, null=True)
    content_category = models.CharField(max_length=100, blank=True, null=True)
    platform_specific_behavior = models.JSONField(default=dict, blank=True)

    additional_attributes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.item}"
