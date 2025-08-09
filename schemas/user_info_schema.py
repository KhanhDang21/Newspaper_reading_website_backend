from pydantic import BaseModel, EmailStr
from typing import Optional
from beanie import PydanticObjectId

class UserInfoCreate(BaseModel):
    full_name: str
    number_phone: str
    email: EmailStr
    id_personal: str
    status: bool

class UserInfoUpdate(BaseModel):
    full_name: Optional[str]
    number_phone: Optional[str]
    email: Optional[str]
    id_personal: Optional[str]
    status: Optional[bool]

class UserInfoResponse(BaseModel):
    id: PydanticObjectId
    full_name: str
    number_phone: str
    email: str
    id_personal: str
    status: bool

    class Config:
        json_encoders = {
            PydanticObjectId: str
        }