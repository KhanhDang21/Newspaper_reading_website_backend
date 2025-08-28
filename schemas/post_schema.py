from pydantic import BaseModel
from typing import Optional, List
from beanie import PydanticObjectId

class PostCreate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    images: Optional[List[str]] = None
    highlight: Optional[str] = None
    references: Optional[List[str]] = None
    author: Optional[str] = None
    time: Optional[str] = None
    topic: Optional[List[str]] = None

class PostUpdate(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    images: Optional[List[str]] = None
    highlight: Optional[str] = None
    references: Optional[List[str]] = None
    author: Optional[str] = None
    time: Optional[str] = None
    topic: Optional[List[str]] = None

class PostResponse(BaseModel):
    id: PydanticObjectId
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    images: Optional[List[str]] = None
    highlight: Optional[str] = None
    references: Optional[List[str]] = None
    author: Optional[str] = None
    time: Optional[str] = None
    topic: Optional[List[str]] = None
    newspaper_publisher: Optional[PydanticObjectId] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }