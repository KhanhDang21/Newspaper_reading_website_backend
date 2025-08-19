from beanie import Document, Link
from models.user_info_model import UserInfo
from models.post_model import Post

class UserInfoPost(Document):
    user_info: Link[UserInfo]
    post: Link[Post]

    class Settings:
        name = "user_info_post"