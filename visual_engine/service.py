import uuid
import time
from typing import Optional, Dict, Any

from visual_engine.domain import VisualGenerationRequest, VisualGenerationResult, GenerationStatus
from visual_engine.presets import VisualPresets
from visual_engine.prompt_builder import PromptBuilder
from visual_engine.providers import ProviderRegistry
from visual_engine.adapters import PatternLibraryAdapter, MediaStorageAdapter

class VisualEngineService:
    """
    Main orchestration service for the V2 visual-content generation engine.
    Called by Frontend, n8n, and Abrit Agent.
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry,
        pattern_library_adapter: Optional[PatternLibraryAdapter] = None,
        media_storage_adapter: Optional[MediaStorageAdapter] = None
    ):
        self.provider_registry = provider_registry
        self.pattern_library_adapter = pattern_library_adapter
        self.media_storage_adapter = media_storage_adapter

    def generate_visual(self, request: VisualGenerationRequest) -> VisualGenerationResult:
        """
        Orchestrates the generation process:
        1. Enriches request with pattern library data
        2. Applies platform presets (aspect ratio, etc.)
        3. Builds the prompt
        4. Selects a provider
        5. Executes generation
        6. Stores resulting media info via adapter
        """

        # Ensure trace_id exists
        if not request.trace_id:
            request.trace_id = str(uuid.uuid4())

        try:
            # 1. Fetch pattern context if not provided but requested via metadata
            if self.pattern_library_adapter and not request.pattern_library_context:
                pattern_id = request.metadata.get("pattern_id")
                if pattern_id:
                    request.pattern_library_context = self.pattern_library_adapter.get_pattern_context(pattern_id)

            # 2. Apply Platform Presets if missing
            platform_preset = VisualPresets.get_platform_preset(request.platform)
            if not request.aspect_ratio and platform_preset:
                request.aspect_ratio = platform_preset.get("aspect_ratio")
            if not request.dimensions and platform_preset:
                request.dimensions = platform_preset.get("dimensions")

            # 3. Build comprehensive prompt
            final_prompt = PromptBuilder.build(request)

            # 4. Get available provider
            try:
                provider = self.provider_registry.get_provider(request.preferred_provider)
            except RuntimeError as e:
                return VisualGenerationResult(
                    status=GenerationStatus.UNAVAILABLE,
                    request=request,
                    error_message=str(e),
                    trace_id=request.trace_id
                )

            # 5. Execute generation
            result = provider.generate(request, final_prompt)

            # 6. Store media tracking info if successful and adapter exists
            if result.status == GenerationStatus.SUCCESS and result.media_url and self.media_storage_adapter:
                # Typically we would download the image or pass the URL for the adapter to ingest.
                # Here we register metadata for the generated URL.
                storage_metadata = {
                    "provider": result.provider_used,
                    "model": result.model_used,
                    "dimensions": request.dimensions,
                    "workspace_id": request.workspace_id,
                    "related_content_id": request.related_content_id,
                    "timestamp": time.time()
                }
                self.media_storage_adapter.register_metadata(result.media_url, storage_metadata)

            return result

        except Exception as e:
            return VisualGenerationResult(
                status=GenerationStatus.FAILED,
                request=request,
                error_message=f"Internal service error: {str(e)}",
                trace_id=request.trace_id
            )
