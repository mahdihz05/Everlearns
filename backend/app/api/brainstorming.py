from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/brainstorming", tags=["Brainstorming"])

# Pydantic models for request/response validation
class TopicSuggestionRequest(BaseModel):
    workspace_id: int

class AngleRequest(BaseModel):
    workspace_id: int
    topic: str

class IdeaCreate(BaseModel):
    workspace_id: int
    topic: str
    angle: str
    suggested_platform: str = "Twitter"

# Mock dependency injection for services
def get_brainstorming_service():
    from app.services.brainstorming_service import BrainstormingService
    from app.services.adapters import ContentHistoryAdapter, WorkspaceMemoryAdapter, ContentPatternLibraryAdapter
    from app.services.search import WebSearchProvider

    return BrainstormingService(
        ContentHistoryAdapter(),
        WorkspaceMemoryAdapter(),
        ContentPatternLibraryAdapter(),
        WebSearchProvider()
    )

@router.post("/suggestions", response_model=List[Dict[str, str]])
def get_suggestions(request: TopicSuggestionRequest, service = Depends(get_brainstorming_service)):
    return service.generate_topic_suggestions(request.workspace_id)

@router.post("/angles", response_model=List[Dict[str, str]])
def get_angles(request: AngleRequest, service = Depends(get_brainstorming_service)):
    return service.generate_angles(request.topic, request.workspace_id)

@router.post("/ideas")
def create_idea(idea: IdeaCreate):
    # In a real app, this would save to the DB using the SQLAlchemy models
    return {"status": "success", "idea_id": 1, "data": idea.model_dump()}
