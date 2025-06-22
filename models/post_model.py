from typing import Optional
from beanie import Document, Link
from models.user_info_model import UserInfo


class Post(Document):
    title: str
    content: str
    #user_info_id: Link["UserInfo"]
    link_URL: Optional[str] = None
    tags: Optional[list[str]] = None

    class Settings:
        name = "post"
