from rest_framework import serializers
from .models import Workspace, AgentSession, Message, ToolCall, ToolResult

class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = '__all__'

class AgentSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSession
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ToolCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolCall
        fields = '__all__'

class ToolResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolResult
        fields = '__all__'
