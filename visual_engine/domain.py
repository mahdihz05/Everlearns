from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List

class VisualType(Enum):
    SIMPLE_IMAGE = "simple_image"
    POSTER = "poster"
    CONTENT_COVER = "content_cover"
    EDUCATIONAL = "educational"
    NEWS = "news"
    ADVERTISEMENT = "advertisement"
    TEXT_CONTAINING = "text_containing"

class Platform(Enum):
    TELEGRAM = "telegram"
    LINKEDIN = "linkedin"
    WORDPRESS = "wordpress"
    GENERIC = "generic"

class GenerationStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    UNAVAILABLE = "unavailable"

@dataclass
class VisualGenerationRequest:
    workspace_id: str
    prompt: str
    visual_type: VisualType
    platform: Platform = Platform.GENERIC
    related_content_id: Optional[str] = None
    aspect_ratio: Optional[str] = None
    dimensions: Optional[Dict[str, int]] = None
    text_mode: bool = False
    brand_context: Optional[Dict[str, Any]] = None
    pattern_library_context: Optional[Dict[str, Any]] = None
    preferred_provider: Optional[str] = None
    preferred_model: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None

@dataclass
class VisualGenerationResult:
    status: GenerationStatus
    request: VisualGenerationRequest
    media_url: Optional[str] = None
    media_path: Optional[str] = None
    provider_used: Optional[str] = None
    model_used: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    trace_id: Optional[str] = None
