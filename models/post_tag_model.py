from typing import Optional
from beanie import Document, Link
from models.post_model import Post
from models.tag_model import Tag  

class PostTag(Document):
    post: Link[Post]
    tag: Link[Tag]

    class Settings:
        name = "post_tag"