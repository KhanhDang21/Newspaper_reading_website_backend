from pydantic import BaseModel
from typing import Optional, List
from beanie import PydanticObjectId

class PostCreate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    image_URL: Optional[str] = None
    highlight: Optional[str] = None
    references: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[str] = None
    topic: Optional[str] = None

class PostUpdate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    image_URL: Optional[str] = None
    highlight: Optional[str] = None
    references: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[str] = None
    topic: Optional[str] = None

class PostResponse(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    image_URL: Optional[str] = None
    highlight: Optional[str] = None
    references: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[str] = None
    topic: Optional[str] = None
    newspaper_publisher: Optional[PydanticObjectId] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }