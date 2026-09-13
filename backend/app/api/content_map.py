from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/content-map", tags=["Content Map"])

class RecommendMapRequest(BaseModel):
    workspace_id: int
    ideas: List[Dict[str, Any]]

def get_recommendation_service():
    from app.services.recommendation_service import RecommendationService
    from app.services.adapters import ContentHistoryAdapter, WorkspaceMemoryAdapter

    return RecommendationService(
        ContentHistoryAdapter(),
        WorkspaceMemoryAdapter()
    )

@router.post("/recommend")
def recommend_content_map(request: RecommendMapRequest, service = Depends(get_recommendation_service)):
    items = service.recommend_schedule(request.ideas)
    return {"status": "success", "map_items": items}

@router.post("/handoff/{target}")
def handoff_to_execution(target: str, map_id: int):
    """
    Handoff to execution layers like n8n or Agent.
    """
    valid_targets = ["n8n", "agent", "scheduler"]
    if target not in valid_targets:
        raise HTTPException(status_code=400, detail="Invalid handoff target")

    # In reality, this would trigger a webhook or event
    return {"status": "handoff_initiated", "target": target, "map_id": map_id}
