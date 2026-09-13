from typing import Dict, Any, Optional
from .registry import ToolMetadata
from .models import Workspace, PermissionPolicy

PERMISSION_ALLOW_ONCE = "Allow Once"
PERMISSION_DENY = "Deny"
PERMISSION_ALWAYS_ALLOW = "Always Allow"

class PermissionEnforcer:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id

    def get_permission_requirement(self, tool: ToolMetadata) -> str:
        # Default behavior relies on the tool metadata's required permission
        return tool.required_permission

    def resolve_policy(self, tool_id: str) -> Optional[str]:
        # Resolve saved policy for the specific tool and workspace
        try:
            policy_obj = PermissionPolicy.objects.get(workspace_id=self.workspace_id, tool_identifier=tool_id)
            return policy_obj.policy
        except PermissionPolicy.DoesNotExist:
            return None

    def enforce(self, tool: ToolMetadata) -> Dict[str, Any]:
        """
        Enforce permissions before executing a tool.
        Returns a dict with 'allowed' (bool) and 'reason' (str) or 'action_required' (str).
        """
        policy = self.resolve_policy(tool.identifier)

        # If explicitly denied
        if policy == PERMISSION_DENY:
            return {"allowed": False, "reason": f"Tool '{tool.name}' is explicitly denied."}

        # If explicitly always allowed
        if policy == PERMISSION_ALWAYS_ALLOW:
            return {"allowed": True, "reason": "Always allowed via saved policy."}

        # If it's a one-time allowance that was just granted, we can allow it
        if policy == PERMISSION_ALLOW_ONCE:
            # Consume the allow once policy
            PermissionPolicy.objects.filter(workspace_id=self.workspace_id, tool_identifier=tool.identifier).delete()
            return {"allowed": True, "reason": "Allowed for this single execution."}

        # Default fallback based on tool metadata requirement
        req = self.get_permission_requirement(tool)

        if req == PERMISSION_ALWAYS_ALLOW:
            return {"allowed": True, "reason": "Default always allow."}
        elif req == PERMISSION_ALLOW_ONCE:
            # Need to request approval
            return {"allowed": False, "action_required": "request_approval", "reason": f"Tool '{tool.name}' requires explicit approval."}
        else:
            return {"allowed": False, "reason": f"Unknown permission requirement: {req}"}
