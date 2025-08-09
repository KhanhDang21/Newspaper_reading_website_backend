from typing import Optional
from beanie import Document, Link

class UserInfo(Document):
    full_name: str
    number_phone: Optional[str] = None
    email: str
    id_personal: Optional[str] = None
    status: bool

    class Settings:
        name = "user_info"
