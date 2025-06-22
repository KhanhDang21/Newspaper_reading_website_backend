from typing import Optional
from beanie import Document, Link
from models.user_authentication_model import UserAuthentication

class UserInfo(Document):
    user_id: Link[UserAuthentication]
    full_name: str
    number_phone: Optional[str] = None
    email: str
    id_personal: Optional[str] = None
    role: Optional[str] = None
    status: bool

    class Settings:
        name = "user_info"
