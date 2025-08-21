from pydantic import BaseModel
from beanie import Document, PydanticObjectId

class UserInfoTagCreate(BaseModel):
    tag: PydanticObjectId
    
class UserInfoTagResponse(BaseModel):
    id: PydanticObjectId
    user_info: PydanticObjectId
    tag: PydanticObjectId

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }