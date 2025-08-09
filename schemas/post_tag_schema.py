from pydantic import BaseModel
from beanie import PydanticObjectId

class PostTagCreate(BaseModel):
    post: PydanticObjectId
    tag: PydanticObjectId

class PostTagUpdate(BaseModel):
    post: PydanticObjectId
    tag: PydanticObjectId

class PostTagResponse(BaseModel):
    id: PydanticObjectId
    post: PydanticObjectId
    tag: PydanticObjectId

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }