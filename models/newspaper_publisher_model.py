from typing import Optional, List
from beanie import Document

class NewspaperPublisher(Document):
    name: str
    domain: str
    country: str
    description: Optional[str] = None

    class Settings:
        name = "newspaper_publisher"