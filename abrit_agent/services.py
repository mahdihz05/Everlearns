from typing import Dict, Any, List, Optional
from django.utils import timezone
from .models import AgentSession, Message, ToolCall, ToolResult
from .registry import ToolRegistry
from .permissions import PermissionEnforcer

class AgentService:
    def __init__(self, session: AgentSession):
        self.session = session
        self.workspace_id = str(session.workspace.id)
        self.permission_enforcer = PermissionEnforcer(self.workspace_id)

    def process_message(self, content: str, user_metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Main entry point for a user message.
        """
        # 1. Save user message
        user_msg = Message.objects.create(
            session=self.session,
            role='user',
            content=content,
            metadata=user_metadata or {}
        )

        # 2. Obtain relevant workspace context (simulated here)
        # Normally would call a LLM here to decide which tools to use.
        # For demonstration of architecture, we'll return a simple response
        # or simulate a tool call.

        # In a real scenario, this is where we'd interface with the LLM or modular workflow.
        # We'll just return a direct agent message for now, acknowledging the context.
        agent_msg = Message.objects.create(
            session=self.session,
            role='agent',
            content=f"Received your request: {content}. Analyzing context..."
        )

        return {
            "status": "success",
            "message_id": str(agent_msg.id),
            "response": agent_msg.content
        }

    def execute_tool(self, message_id: str, tool_identifier: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool on behalf of the agent.
        """
        try:
            message = Message.objects.get(id=message_id, session=self.session)
        except Message.DoesNotExist:
            return {"status": "error", "error": "Message not found."}

        tool = ToolRegistry.get_tool(tool_identifier)
        if not tool:
            return {"status": "error", "error": f"Tool {tool_identifier} not found in registry."}

        # Create ToolCall record
        tool_call = ToolCall.objects.create(
            message=message,
            tool_name=tool_identifier,
            arguments=arguments,
            status='pending'
        )

        # 3. Enforce permission policy
        perm_result = self.permission_enforcer.enforce(tool)
        if not perm_result["allowed"]:
            if perm_result.get("action_required") == "request_approval":
                tool_call.status = 'pending'
                tool_call.save()
                return {
                    "status": "pending_approval",
                    "tool_call_id": str(tool_call.id),
                    "reason": perm_result["reason"]
                }
            else:
                tool_call.status = 'denied'
                tool_call.error_message = perm_result["reason"]
                tool_call.save()
                return {
                    "status": "denied",
                    "tool_call_id": str(tool_call.id),
                    "reason": perm_result["reason"]
                }

        # 4. Check availability
        if not tool.availability:
            tool_call.status = 'failed'
            tool_call.error_message = "Tool is currently unavailable."
            tool_call.save()
            return {
                "status": "unavailable",
                "tool_call_id": str(tool_call.id),
                "error": "Tool is currently unavailable."
            }

        # 5. Execute Tool
        tool_call.status = 'executing'
        tool_call.save()

        start_time = timezone.now()
        output = {}
        error_msg = ""
        try:
            if tool.executor:
                output = tool.executor(**arguments)
            else:
                error_msg = "No executor defined."
        except Exception as e:
            error_msg = tool.error_normalizer(e) if tool.error_normalizer else str(e)

        end_time = timezone.now()
        execution_time_ms = int((end_time - start_time).total_seconds() * 1000)

        if error_msg:
            tool_call.status = 'failed'
            tool_call.error_message = error_msg
        else:
            tool_call.status = 'completed'

        tool_call.save()

        # 6. Record ToolResult
        ToolResult.objects.create(
            tool_call=tool_call,
            output=output,
            error=error_msg,
            execution_time_ms=execution_time_ms
        )

        return {
            "status": tool_call.status,
            "tool_call_id": str(tool_call.id),
            "output": output,
            "error": error_msg
        }
