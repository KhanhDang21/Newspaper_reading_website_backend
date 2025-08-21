from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId

class CommentCreate(BaseModel):
    post: Optional[PydanticObjectId] = None
    content: Optional[str] = None

class CommentUpdate(BaseModel):
    post: Optional[PydanticObjectId] = None
    content: Optional[str] = None

class CommentResponse(BaseModel):
    id: PydanticObjectId
    post: PydanticObjectId
    user_info: PydanticObjectId
    content: Optional[str] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }