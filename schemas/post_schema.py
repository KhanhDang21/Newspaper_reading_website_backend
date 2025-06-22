from pydantic import BaseModel
from typing import Optional, List
from beanie import PydanticObjectId

class PostCreate(BaseModel):
    title: str
    content: str
    link_url: Optional[str] = None
    tags: Optional[list[str]] = None

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    link_url: Optional[str]
    tags: Optional[List[str]] = None

class PostResponse(BaseModel):
    title: str
    content: str
    link_url: Optional[str] = None
    tags: Optional[List[str]] = None
