from typing import Dict, Any, List
from .models import GenerationRequest, GenerationResult
from .providers import BaseAIProvider
from .prompts import compose_prompt
from .platforms import get_platform_strategy
from .adapters import PatternLibraryAdapter, ContentHistoryAdapter, MemoryAdapter

class ContentEngine:
    def __init__(self, provider: BaseAIProvider):
        self.provider = provider
        self.pattern_adapter = PatternLibraryAdapter()
        self.history_adapter = ContentHistoryAdapter()
        self.memory_adapter = MemoryAdapter()

    def _gather_context(self, request: GenerationRequest) -> Dict[str, Any]:
        context = request.model_dump()

        # Merge platform rules
        if request.platform:
            platform_rules = get_platform_strategy(request.platform).get_platform_rules()
            existing_instructions = context.get("additional_instructions") or ""
            context["additional_instructions"] = (existing_instructions + "\n" + str(platform_rules)).strip()

        # Merge memory
        if request.workspace_id:
            memory = self.memory_adapter.get_workspace_rules(request.workspace_id)
            if memory.get("preferred_tone"):
                context["tone"] = memory["preferred_tone"]
            context["memory_context"] = memory.get("brand_rules", [])

        # Merge history
        if request.workspace_id and request.topic:
            history = self.history_adapter.get_recent_content(request.workspace_id, request.topic)
            context["content_history_context"] = history

        # Merge pattern library
        patterns = self.pattern_adapter.get_patterns(
            platform=request.platform,
            topic=request.topic,
            tone=context.get("tone")
        )
        context["pattern_library_context"] = patterns

        return context

    def generate_content(self, request: GenerationRequest) -> GenerationResult:
        context = self._gather_context(request)
        prompt, prompt_version = compose_prompt("system_default", context)

        response = self.provider.generate(prompt, model=request.model)

        return GenerationResult(
            generated_text=response.get("text", ""),
            provider=response.get("provider"),
            model=response.get("model"),
            prompt_version=prompt_version,
            source_context=context
        )

    def generate_title(self, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = "Generate ONLY a catchy title for the following topic."
        return self.generate_content(request)

    def generate_scenario(self, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = "Generate a scenario outline or storyboard based on the topic."
        return self.generate_content(request)

    def rewrite_text(self, text: str, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = f"Rewrite the following text according to the tone and rules:\n{text}"
        return self.generate_content(request)

    def summarize_text(self, text: str, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = f"Summarize the following text:\n{text}"
        return self.generate_content(request)

    def generate_cta(self, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = "Generate ONLY a Call To Action (CTA) for the following topic."
        return self.generate_content(request)

    def generate_hashtags(self, request: GenerationRequest) -> GenerationResult:
        request.additional_instructions = "Generate ONLY a list of relevant hashtags for the following topic, space separated."
        result = self.generate_content(request)
        # Simple split logic for hashtags
        hashtags = [h.strip() for h in result.generated_text.split() if h.startswith('#')]
        if not hashtags:
            # Fallback if the model didn't add #
            hashtags = [f"#{h.strip()}" for h in result.generated_text.split()]
        result.hashtags = hashtags
        return result
