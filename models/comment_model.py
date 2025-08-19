from beanie import Document, Link
from typing import Optional

from models.post_model import Post
from models.user_info_model import UserInfo

class Comment(Document):
    post_id: Link[Post]
    user_info_id: Link[UserInfo]
    content: Optional[str] = None

    class Settings:
        name = "comment"