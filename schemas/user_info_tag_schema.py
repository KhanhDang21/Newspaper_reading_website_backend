from pydantic import BaseModel
from beanie import Document, PydanticObjectId

class UserInfoTagCreate(BaseModel):
    tag_id: PydanticObjectId
    
class UserInfoTagResponse(BaseModel):
    id: PydanticObjectId
    user_id: PydanticObjectId
    tag_id: PydanticObjectId

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }