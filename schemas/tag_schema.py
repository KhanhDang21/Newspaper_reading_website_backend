from pydantic import BaseModel
from typing import Optional, List
from beanie import Document, PydanticObjectId

class TagCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TagUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str] = None

class TagResponse(BaseModel):
    id: PydanticObjectId
    name: str
    description: Optional[str] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }