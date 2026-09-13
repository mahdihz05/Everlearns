from django.db import models
from .enums import MemoryCategory

class WorkspaceMemory(models.Model):
    workspace_id = models.UUIDField(db_index=True)
    category = models.CharField(max_length=50, choices=[(tag.value, tag.name) for tag in MemoryCategory])
    text_value = models.TextField(blank=True, null=True)
    structured_value = models.JSONField(blank=True, null=True)
    confidence = models.FloatField(default=1.0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['workspace_id', 'category']),
            models.Index(fields=['workspace_id', 'active']),
        ]

    def __str__(self):
        return f"{self.workspace_id} - {self.category} (Active: {self.active})"
