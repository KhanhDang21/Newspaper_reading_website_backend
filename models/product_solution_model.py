from typing import Optional, List
from beanie import Document

class ProductSolution(Document):
    name: str
    field: str
    des: str
    tags: Optional[List[str]] = None
    supplier: str
    website: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None

    class Settings:
        name = "product_solution"