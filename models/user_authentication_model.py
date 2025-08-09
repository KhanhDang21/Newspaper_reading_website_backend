from pydantic import Field
from beanie import Document, Link
from models.user_info_model import UserInfo
from typing import Optional


class UserAuthentication(Document):
    username: str = Field(..., unique = True)
    hashed_password: str
    user_info: Optional[Link[UserInfo]] = None

    class Settings:
        name = "user_authentication"