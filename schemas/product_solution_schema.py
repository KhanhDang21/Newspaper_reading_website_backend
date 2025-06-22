from pydantic import BaseModel
from typing import Optional
from beanie import Document, Link

class ProductSolutionCreate(BaseModel):
    name: str
    field: str
    des: str
    tag: Optional[str] = None
    supplier: str
    website: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None

class ProductSolutionUpdate(BaseModel):
    name: Optional[str]
    field: Optional[str]
    des: Optional[str]
    tag: Optional[str]
    supplier: Optional[str]
    website: Optional[str]
    contact_info: Optional[str]
    address: Optional[str]

class ProductSolutionResponse(BaseModel):
    name: str
    field: str
    des: str
    tag: Optional[str] = None
    supplier: str
    website: Optional[str] = None
    contact_info: Optional[str] = None
    address: Optional[str] = None
