from typing import Dict, Any, Optional, List

class PromptTemplate:
    def __init__(self, template: str, version: str = "1.0", name: str = "base"):
        self.template = template
        self.version = version
        self.name = name

    def render(self, **kwargs) -> str:
        # Simple format-based rendering
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            # Fallback for missing keys
            return self.template + f"\n[Missing context: {e}]"


class PromptRegistry:
    def __init__(self):
        self._prompts: Dict[str, PromptTemplate] = {}

    def register(self, template: PromptTemplate):
        self._prompts[template.name] = template

    def get(self, name: str) -> Optional[PromptTemplate]:
        return self._prompts.get(name)

# A default generic template as a fallback
default_system_prompt = PromptTemplate(
    name="system_default",
    version="1.0",
    template=(
        "You are a professional content generator.\n"
        "Topic: {topic}\n"
        "Platform: {platform}\n"
        "Goal: {goal}\n"
        "Audience: {audience}\n"
        "Tone: {tone}\n"
        "Brand Rules: {brand_rules}\n"
        "Memory Context: {memory_context}\n"
        "History Context: {content_history_context}\n"
        "Pattern Rules: {pattern_context}\n"
        "Additional Instructions: {additional_instructions}\n\n"
        "Generate the requested content."
    )
)

registry = PromptRegistry()
registry.register(default_system_prompt)

def compose_prompt(
    base_template_name: str,
    context: Dict[str, Any],
    registry_instance: PromptRegistry = registry
) -> tuple[str, str]:
    """
    Composes a prompt from a template and context.
    Returns (rendered_prompt, prompt_version).
    """
    template = registry_instance.get(base_template_name)
    if not template:
        template = registry_instance.get("system_default")

    # Ensure all expected keys are in context with safe defaults
    safe_context = {
        "topic": context.get("topic", "N/A"),
        "platform": context.get("platform", "General"),
        "goal": context.get("goal", "Inform"),
        "audience": context.get("audience", "General Audience"),
        "tone": context.get("tone", "Professional"),
        "brand_rules": ", ".join(context.get("brand_rules", [])),
        "memory_context": ", ".join(context.get("memory_context", [])),
        "content_history_context": ", ".join(context.get("content_history_context", [])),
        "pattern_context": str(context.get("pattern_library_context", {})),
        "additional_instructions": context.get("additional_instructions") or "None"
    }

    return template.render(**safe_context), template.version
