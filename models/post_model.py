from typing import Optional
from beanie import Document, Link
from models.newspaper_publisher_model import NewspaperPublisher

class Post(Document):
    title: str
    content: str
    summary: Optional[str] = None
    domain: Optional[str] = None
    image_URL: Optional[str] = None
    highlight: Optional[str] = None
    references: Optional[str] = None
    author: Optional[str] = None
    timestamp: Optional[str] = None
    topic: Optional[str] = None
    newspaper_publisher: Optional[Link[NewspaperPublisher]] = None

    class Settings:
        name = "post"
