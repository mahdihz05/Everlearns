from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Workspace, AgentSession, Message, ToolCall, PermissionPolicy
from .serializers import WorkspaceSerializer, AgentSessionSerializer, MessageSerializer, ToolCallSerializer
from .services import AgentService

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

class AgentSessionViewSet(viewsets.ModelViewSet):
    queryset = AgentSession.objects.all()
    serializer_class = AgentSessionSerializer

    @action(detail=True, methods=['post'])
    def converse(self, request, pk=None):
        session = self.get_object()
        content = request.data.get('content')
        metadata = request.data.get('metadata', {})

        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        service = AgentService(session)
        result = service.process_message(content, metadata)

        return Response(result)

    @action(detail=True, methods=['post'])
    def execute_tool(self, request, pk=None):
        session = self.get_object()
        message_id = request.data.get('message_id')
        tool_identifier = request.data.get('tool_identifier')
        arguments = request.data.get('arguments', {})

        if not message_id or not tool_identifier:
            return Response({"error": "message_id and tool_identifier are required"}, status=status.HTTP_400_BAD_REQUEST)

        service = AgentService(session)
        result = service.execute_tool(message_id, tool_identifier, arguments)

        return Response(result)

class ToolCallViewSet(viewsets.ModelViewSet):
    queryset = ToolCall.objects.all()
    serializer_class = ToolCallSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        tool_call = self.get_object()
        if tool_call.status != 'pending':
            return Response({"error": "Only pending tool calls can be approved"}, status=status.HTTP_400_BAD_REQUEST)

        # Save a one-time permission policy
        workspace = tool_call.message.session.workspace
        PermissionPolicy.objects.update_or_create(
            workspace=workspace,
            tool_identifier=tool_call.tool_name,
            defaults={'policy': 'Allow Once'}
        )

        tool_call.status = 'approved'
        tool_call.save()
        return Response({"status": "approved", "tool_call_id": str(tool_call.id)})

    @action(detail=True, methods=['post'])
    def deny(self, request, pk=None):
        tool_call = self.get_object()
        if tool_call.status != 'pending':
            return Response({"error": "Only pending tool calls can be denied"}, status=status.HTTP_400_BAD_REQUEST)

        tool_call.status = 'denied'
        tool_call.error_message = "Denied by user."
        tool_call.save()
        return Response({"status": "denied", "tool_call_id": str(tool_call.id)})
