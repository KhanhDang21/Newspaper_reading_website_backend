from pydantic import BaseModel
from beanie import PydanticObjectId

class UserInfoPostCreate(BaseModel):
    post: PydanticObjectId

class UserInfoPostResponse(BaseModel):
    id: PydanticObjectId
    user_info: PydanticObjectId
    post: PydanticObjectId

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }