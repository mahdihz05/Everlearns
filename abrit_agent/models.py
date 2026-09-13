import uuid
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Workspace(BaseModel):
    name = models.CharField(max_length=255)
    # Using a simple workspace model as a placeholder since it's a foundation

    def __str__(self):
        return self.name

class AgentSession(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='agent_sessions')
    title = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default='active') # active, closed
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Session {self.id} in {self.workspace}"

class Message(BaseModel):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('agent', 'Agent'),
        ('system', 'System'),
        ('tool', 'Tool'),
    )

    session = models.ForeignKey(AgentSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.role} message in {self.session.id}"

class ToolCall(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
        ('executing', 'Executing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='tool_calls')
    tool_name = models.CharField(max_length=255)
    arguments = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    trace_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Call to {self.tool_name} (Status: {self.status})"

class ToolResult(BaseModel):
    tool_call = models.OneToOneField(ToolCall, on_delete=models.CASCADE, related_name='result')
    output = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)
    execution_time_ms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Result for {self.tool_call.tool_name}"


class PermissionPolicy(BaseModel):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='permission_policies')
    tool_identifier = models.CharField(max_length=255)
    policy = models.CharField(max_length=50) # 'Allow Once', 'Deny', 'Always Allow'

    class Meta:
        unique_together = ('workspace', 'tool_identifier')

    def __str__(self):
        return f"{self.policy} for {self.tool_identifier} in {self.workspace.name}"
