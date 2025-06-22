from beanie import PydanticObjectId
from pydantic import BaseModel


class UserAuthentication(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class AdminPasswordUpdate(BaseModel):
    user_id: PydanticObjectId
    new_password: str