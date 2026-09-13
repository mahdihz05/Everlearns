from typing import Dict, Any, Optional
from visual_engine.domain import VisualType, Platform

class VisualPresets:
    @staticmethod
    def get_type_config(visual_type: VisualType) -> Dict[str, Any]:
        configs = {
            VisualType.SIMPLE_IMAGE: {
                "text_mode": False,
                "complexity": "low",
                "focus": "subject"
            },
            VisualType.POSTER: {
                "text_mode": True,
                "complexity": "high",
                "focus": "typography and layout",
                "style": "bold"
            },
            VisualType.CONTENT_COVER: {
                "text_mode": True,
                "complexity": "medium",
                "focus": "title and main graphic"
            },
            VisualType.EDUCATIONAL: {
                "text_mode": True,
                "complexity": "medium",
                "focus": "clarity and information"
            },
            VisualType.NEWS: {
                "text_mode": True,
                "complexity": "high",
                "focus": "factual and current"
            },
            VisualType.ADVERTISEMENT: {
                "text_mode": True,
                "complexity": "high",
                "focus": "product and call to action",
                "style": "persuasive"
            },
            VisualType.TEXT_CONTAINING: {
                "text_mode": True,
                "complexity": "medium",
                "focus": "text readability"
            }
        }
        return configs.get(visual_type, {})

    @staticmethod
    def get_platform_preset(platform: Platform) -> Dict[str, Any]:
        presets = {
            Platform.TELEGRAM: {
                "aspect_ratio": "1:1",
                "dimensions": {"width": 1080, "height": 1080},
                "recommended_format": "jpeg"
            },
            Platform.LINKEDIN: {
                "aspect_ratio": "1200:627",
                "dimensions": {"width": 1200, "height": 627},
                "recommended_format": "png"
            },
            Platform.WORDPRESS: {
                "aspect_ratio": "16:9",
                "dimensions": {"width": 1200, "height": 675},
                "recommended_format": "webp"
            },
            Platform.GENERIC: {
                "aspect_ratio": "1:1",
                "dimensions": {"width": 1024, "height": 1024},
                "recommended_format": "png"
            }
        }
        return presets.get(platform, presets[Platform.GENERIC])
