from typing import Dict, Any

class BasePlatformStrategy:
    def get_platform_rules(self) -> Dict[str, Any]:
        return {
            "length": "medium",
            "formatting": "standard",
            "tone_adjustment": None,
            "cta_style": "standard"
        }

class TelegramStrategy(BasePlatformStrategy):
    def get_platform_rules(self) -> Dict[str, Any]:
        return {
            "length": "short-to-medium",
            "formatting": "bullet points, emojis",
            "tone_adjustment": "conversational and direct",
            "cta_style": "inline link or direct message prompt"
        }

class LinkedInStrategy(BasePlatformStrategy):
    def get_platform_rules(self) -> Dict[str, Any]:
        return {
            "length": "medium-to-long",
            "formatting": "short paragraphs, structured hook",
            "tone_adjustment": "professional, insightful, networking-focused",
            "cta_style": "question to engage comments"
        }

class WordPressStrategy(BasePlatformStrategy):
    def get_platform_rules(self) -> Dict[str, Any]:
        return {
            "length": "long",
            "formatting": "HTML headings (H2, H3), paragraphs, lists",
            "tone_adjustment": "informative, SEO-friendly",
            "cta_style": "newsletter signup or related article link"
        }

def get_platform_strategy(platform_name: str) -> BasePlatformStrategy:
    strategies = {
        "telegram": TelegramStrategy(),
        "linkedin": LinkedInStrategy(),
        "wordpress": WordPressStrategy()
    }
    return strategies.get(platform_name.lower(), BasePlatformStrategy())
