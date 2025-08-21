from beanie import Document, Link
from models.user_info_model import UserInfo
from models.tag_model import Tag

class UserInfoTag(Document):
    user_info: Link[UserInfo]
    tag: Link[Tag]

    class Settings:
        name = "user_info_tag"
