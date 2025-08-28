from typing import Optional, List
from beanie import Document, Link
from models.newspaper_publisher_model import NewspaperPublisher

class Post(Document):
    title: Optional[str]
    content: Optional[str]
    summary: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    images: Optional[List[str]] = None
    highlight: Optional[str] = None
    references: Optional[List[str]] = None
    author: Optional[str] = None
    time: Optional[str] = None
    topic: Optional[List[str]] = None
    newspaper_publisher: Optional[Link[NewspaperPublisher]] = None

    class Settings:
        name = "post"

