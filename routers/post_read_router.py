from fastapi import APIRouter, Depends, HTTPException
from configs.authentication import get_current_user
from services.post_read_service import get_post_read_service
from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/read-post",
    tags=["read-post"]
)

class PostReadResponse(BaseModel):
    status: str
    data: Optional[List[str]] = None
    message: Optional[str] = None

@router.post("/{post_id}/read", response_model=PostReadResponse)
def mark_post_as_read(
    post_id: PydanticObjectId, 
    current_user = Depends(get_current_user),
    service = Depends(get_post_read_service)
):
    result = service.mark_post_as_read(str(post_id), current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/all", response_model=PostReadResponse)
def get_all_read_posts(
    current_user = Depends(get_current_user), 
    service = Depends(get_post_read_service)
):
    result = service.get_all_read_posts(current_user)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result
