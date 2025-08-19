from pydantic import BaseModel
from typing import Optional, List
from beanie import Document, PydanticObjectId

class CommentCreate(BaseModel):
    post_id: Optional[PydanticObjectId] = None
    content: Optional[str] = None

class CommentUpdate(BaseModel):
    post_id: Optional[PydanticObjectId] = None
    content: Optional[str] = None

class CommentResponse(BaseModel):
    id: PydanticObjectId
    post_id: PydanticObjectId
    user_info_id: PydanticObjectId
    content: Optional[str] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }