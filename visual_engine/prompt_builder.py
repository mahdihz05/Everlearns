from typing import List
from visual_engine.domain import VisualGenerationRequest
from visual_engine.presets import VisualPresets

class PromptBuilder:
    """Builds a comprehensive visual generation prompt based on request parameters."""

    @staticmethod
    def build(request: VisualGenerationRequest) -> str:
        parts: List[str] = []

        # 1. Base Prompt
        parts.append(f"Generate an image based on this core concept: {request.prompt}")

        # 2. Visual Type Config
        type_config = VisualPresets.get_type_config(request.visual_type)
        if type_config:
            parts.append(f"Visual Focus: {type_config.get('focus', 'general')}.")
            if 'style' in type_config:
                parts.append(f"Style instruction: {type_config['style']}.")

        # 3. Text Mode Constraint
        text_mode = type_config.get("text_mode", False) or request.text_mode
        if not text_mode:
            parts.append("IMPORTANT: Do NOT include any text, letters, or words in the image.")
        else:
            parts.append("The image may contain text. Make sure typography is clean and readable if applicable.")

        # 4. Aspect Ratio / Dimensions
        if request.aspect_ratio:
            parts.append(f"Aspect Ratio Constraint: {request.aspect_ratio}.")

        # 5. Brand Context
        if request.brand_context:
            brand_colors = request.brand_context.get('colors', [])
            brand_mood = request.brand_context.get('mood', '')
            if brand_colors:
                parts.append(f"Use the following brand colors primarily: {', '.join(brand_colors)}.")
            if brand_mood:
                parts.append(f"The overall mood should be: {brand_mood}.")

        # 6. Pattern Library Context
        if request.pattern_library_context:
            pattern_style = request.pattern_library_context.get('style_pattern', '')
            layout_pattern = request.pattern_library_context.get('layout_pattern', '')
            if pattern_style:
                parts.append(f"Apply visual style pattern: {pattern_style}.")
            if layout_pattern:
                parts.append(f"Follow this layout structure: {layout_pattern}.")

        # 7. Safety / Formatting Constraints
        parts.append("Ensure the visual is safe for general audiences, professional, and high-quality.")

        return " | ".join(parts)
