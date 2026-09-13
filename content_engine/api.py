from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .models import GenerationRequest, GenerationResult
from .operations import ContentEngine
from .providers import DummyAIProvider

router = APIRouter(prefix="/v2/content", tags=["content-engine"])

# In a real app, this would be injected or loaded from config
def get_engine() -> ContentEngine:
    provider = DummyAIProvider(provider_name="default_v2", default_model="dummy-fast-1")
    return ContentEngine(provider=provider)

@router.post("/generate", response_model=GenerationResult)
async def generate_content_api(request: GenerationRequest, engine: ContentEngine = Depends(get_engine)):
    return engine.generate_content(request)

@router.post("/generate-title", response_model=GenerationResult)
async def generate_title_api(request: GenerationRequest, engine: ContentEngine = Depends(get_engine)):
    return engine.generate_title(request)

class RewriteRequest(BaseModel):
    text: str
    context: GenerationRequest

@router.post("/rewrite", response_model=GenerationResult)
async def rewrite_text_api(request: RewriteRequest, engine: ContentEngine = Depends(get_engine)):
    return engine.rewrite_text(request.text, request.context)

@router.post("/generate-hashtags", response_model=GenerationResult)
async def generate_hashtags_api(request: GenerationRequest, engine: ContentEngine = Depends(get_engine)):
    return engine.generate_hashtags(request)

@router.post("/generate-cta", response_model=GenerationResult)
async def generate_cta_api(request: GenerationRequest, engine: ContentEngine = Depends(get_engine)):
    return engine.generate_cta(request)
