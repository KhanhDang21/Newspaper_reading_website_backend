from pydantic import BaseModel
from typing import Optional, List
from beanie import Document, PydanticObjectId

class NewspaperPublisherCreate(BaseModel):
    name: str
    domain: str
    country: str
    description: Optional[str] = None

class NewspaperPublisherUpdate(BaseModel):
    name: Optional[str]
    domain: Optional[str]
    country: Optional[str]
    description: Optional[str] = None

class NewspaperPublisherResponse(BaseModel):
    id: PydanticObjectId
    name: str
    domain: str
    country: str
    description: Optional[str] = None

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }