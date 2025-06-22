from pydantic import Field
from beanie import Document

class UserAuthentication(Document):
    username: str = Field(..., unique = True)
    hashed_password: str

    class Settings:
        name = "user_authentication"