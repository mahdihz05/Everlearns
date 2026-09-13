from typing import Dict, Any, Type, Callable, Optional, List
import inspect

class ToolMetadata:
    def __init__(
        self,
        identifier: str,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        effect_class: str,
        required_permission: str,
        availability: bool = True,
        executor: Optional[Callable] = None,
        error_normalizer: Optional[Callable] = None
    ):
        self.identifier = identifier
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.effect_class = effect_class  # read/analyze, generate/create, modify/write, external/executable/publishing
        self.required_permission = required_permission
        self.availability = availability
        self.executor = executor
        self.error_normalizer = error_normalizer

class ToolRegistry:
    _tools: Dict[str, ToolMetadata] = {}

    @classmethod
    def register(cls, metadata: ToolMetadata):
        cls._tools[metadata.identifier] = metadata

    @classmethod
    def get_tool(cls, identifier: str) -> Optional[ToolMetadata]:
        return cls._tools.get(identifier)

    @classmethod
    def get_all_tools(cls) -> List[ToolMetadata]:
        return list(cls._tools.values())

    @classmethod
    def clear(cls):
        cls._tools = {}

# Effect classes based on requirements
EFFECT_READ = "read/analyze"
EFFECT_GENERATE = "generate/create"
EFFECT_MODIFY = "modify/write"
EFFECT_EXTERNAL = "external/executable/publishing"
