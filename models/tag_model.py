from typing import Optional, List
from beanie import Document

class Tag(Document):
    name: str
    description: Optional[str] = None

    class Settings:
        name = "tag"  