from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAIProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Generate text based on a prompt.
        Should return a dictionary containing at least:
        - 'text': The generated text string
        - 'provider': The name of the provider used
        - 'model': The model used
        - 'usage': Optional usage metadata
        """
        pass

class DummyAIProvider(BaseAIProvider):
    def __init__(self, provider_name: str = "dummy", default_model: str = "dummy-model"):
        self.provider_name = provider_name
        self.default_model = default_model

    def generate(self, prompt: str, model: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        A dummy implementation that echoes back a stub response.
        Useful for fallback or testing.
        """
        used_model = model if model else self.default_model
        return {
            "text": f"Dummy generated content for prompt: {prompt[:50]}...",
            "provider": self.provider_name,
            "model": used_model,
            "usage": {"tokens": 42}
        }
