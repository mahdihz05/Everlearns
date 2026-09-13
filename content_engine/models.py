from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class GenerationRequest(BaseModel):
    workspace_id: Optional[str] = None
    topic: str
    platform: Optional[str] = None
    audience: Optional[str] = None
    goal: Optional[str] = None
    format: Optional[str] = None
    tone: Optional[str] = None
    brand_rules: Optional[List[str]] = Field(default_factory=list)
    content_history_context: Optional[List[str]] = Field(default_factory=list)
    memory_context: Optional[List[str]] = Field(default_factory=list)
    pattern_library_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    model: Optional[str] = None
    provider: Optional[str] = None
    output_language: Optional[str] = "en"
    additional_instructions: Optional[str] = None
    trace_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class GenerationResult(BaseModel):
    generated_text: str
    title: Optional[str] = None
    cta: Optional[str] = None
    hashtags: Optional[List[str]] = Field(default_factory=list)
    provider: Optional[str] = None
    model: Optional[str] = None
    prompt_version: Optional[str] = None
    warnings: Optional[List[str]] = Field(default_factory=list)
    source_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    generated_variants: Optional[List[str]] = Field(default_factory=list)
