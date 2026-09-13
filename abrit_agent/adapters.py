from typing import Dict, Any, Optional
from .registry import (
    ToolRegistry, ToolMetadata,
    EFFECT_READ, EFFECT_GENERATE, EFFECT_MODIFY, EFFECT_EXTERNAL
)

class BaseAdapter:
    def execute(self, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError("This tool is not yet integrated with upstream services.")

    def normalize_error(self, error: Exception) -> str:
        return str(error)

# Define each required tool adapter but mark unimplemented ones as unavailable

class WorkspaceContextAdapter(BaseAdapter):
    pass

class ContentHistoryAdapter(BaseAdapter):
    pass

class MemoryRAGAdapter(BaseAdapter):
    pass

class ContentPatternLibraryAdapter(BaseAdapter):
    pass

class ContentMapAdapter(BaseAdapter):
    pass

class TextGenerationAdapter(BaseAdapter):
    pass

class VisualGenerationAdapter(BaseAdapter):
    pass

class WebSearchAdapter(BaseAdapter):
    pass

class ChannelManagementAdapter(BaseAdapter):
    pass

class PublishingAdapter(BaseAdapter):
    pass

class N8NWorkflowAdapter(BaseAdapter):
    pass

# Register all adapters
def register_all_tools():
    ToolRegistry.register(ToolMetadata(
        identifier="workspace_context",
        name="Workspace Context",
        description="Retrieve context about the current workspace",
        input_schema={"type": "object", "properties": {"workspace_id": {"type": "string"}}},
        output_schema={"type": "object", "properties": {"context": {"type": "string"}}},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False,
        executor=WorkspaceContextAdapter().execute,
        error_normalizer=WorkspaceContextAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="content_history",
        name="Content History",
        description="Retrieve past content history",
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False,
        executor=ContentHistoryAdapter().execute,
        error_normalizer=ContentHistoryAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="memory_rag",
        name="Memory / RAG",
        description="Search workspace memory",
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False,
        executor=MemoryRAGAdapter().execute,
        error_normalizer=MemoryRAGAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="content_pattern_library",
        name="Content Pattern Library",
        description="Retrieve content patterns",
        input_schema={"type": "object", "properties": {"pattern_type": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False,
        executor=ContentPatternLibraryAdapter().execute,
        error_normalizer=ContentPatternLibraryAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="content_map",
        name="Content Map",
        description="Retrieve content map details",
        input_schema={"type": "object", "properties": {"focus_area": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False,
        executor=ContentMapAdapter().execute,
        error_normalizer=ContentMapAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="text_generation",
        name="Text Generation Engine",
        description="Generate text based on a prompt",
        input_schema={"type": "object", "properties": {"prompt": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_GENERATE,
        required_permission="Always Allow",
        availability=False, # upstream not fully implemented
        executor=TextGenerationAdapter().execute,
        error_normalizer=TextGenerationAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="visual_generation",
        name="Visual Generation Engine",
        description="Generate images based on a prompt",
        input_schema={"type": "object", "properties": {"prompt": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_GENERATE,
        required_permission="Always Allow",
        availability=False, # upstream not fully implemented
        executor=VisualGenerationAdapter().execute,
        error_normalizer=VisualGenerationAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="web_search",
        name="Web Search",
        description="Search the web for information",
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_READ,
        required_permission="Always Allow",
        availability=False, # upstream not fully implemented
        executor=WebSearchAdapter().execute,
        error_normalizer=WebSearchAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="channel_management",
        name="Channel Management",
        description="Manage publishing channels",
        input_schema={"type": "object", "properties": {"channel_id": {"type": "string"}, "action": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_MODIFY,
        required_permission="Allow Once",
        availability=False,
        executor=ChannelManagementAdapter().execute,
        error_normalizer=ChannelManagementAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="publishing",
        name="Publishing",
        description="Publish content to a channel",
        input_schema={"type": "object", "properties": {"content_id": {"type": "string"}, "channel": {"type": "string"}, "date": {"type": "string"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_EXTERNAL,
        required_permission="Allow Once",
        availability=False, # upstream not fully implemented
        executor=PublishingAdapter().execute,
        error_normalizer=PublishingAdapter().normalize_error
    ))

    ToolRegistry.register(ToolMetadata(
        identifier="n8n_workflow",
        name="n8n Workflow Execution",
        description="Execute an n8n workflow",
        input_schema={"type": "object", "properties": {"workflow_id": {"type": "string"}, "payload": {"type": "object"}}},
        output_schema={"type": "object"},
        effect_class=EFFECT_EXTERNAL,
        required_permission="Allow Once",
        availability=False,
        executor=N8NWorkflowAdapter().execute,
        error_normalizer=N8NWorkflowAdapter().normalize_error
    ))
