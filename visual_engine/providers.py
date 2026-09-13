from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time

from visual_engine.domain import VisualGenerationRequest, VisualGenerationResult, GenerationStatus

class BaseVisualProvider(ABC):
    """Base interface for all visual generation providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def generate(self, request: VisualGenerationRequest, final_prompt: str) -> VisualGenerationResult:
        """
        Generate visual content based on the request and final constructed prompt.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available (e.g., credentials exist)."""
        pass

class MockVisualProvider(BaseVisualProvider):
    """
    Fallback/Mock provider for when real providers are unavailable or not configured.
    """

    @property
    def provider_name(self) -> str:
        return "mock_provider"

    def is_available(self) -> bool:
        # The mock provider is always available
        return True

    def generate(self, request: VisualGenerationRequest, final_prompt: str) -> VisualGenerationResult:
        # Simulate network delay
        time.sleep(0.5)

        metadata = {
            "mocked": True,
            "simulated_prompt": final_prompt,
            "aspect_ratio_used": request.aspect_ratio
        }

        # If we had a mechanism to determine failure, we'd do it here.
        # For now, always return success with a fake URL

        return VisualGenerationResult(
            status=GenerationStatus.SUCCESS,
            request=request,
            media_url=f"https://mock-provider.local/generated/{request.workspace_id}/image.png",
            provider_used=self.provider_name,
            model_used="mock-model-v1",
            metadata=metadata,
            trace_id=request.trace_id
        )

class ProviderRegistry:
    """Registry to manage and retrieve visual providers."""

    def __init__(self):
        self._providers: Dict[str, BaseVisualProvider] = {}

        # Register default providers
        self.register(MockVisualProvider())

    def register(self, provider: BaseVisualProvider):
        self._providers[provider.provider_name] = provider

    def get_provider(self, name: Optional[str] = None) -> BaseVisualProvider:
        if name and name in self._providers and self._providers[name].is_available():
            return self._providers[name]

        # Fallback logic: return the first available provider (or mock)
        for provider in self._providers.values():
            if provider.is_available():
                return provider

        raise RuntimeError("No visual generation providers available.")
