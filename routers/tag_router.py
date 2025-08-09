from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from services.tag_service import TagServiceFactory
from schemas.tag_schema import TagCreate, TagUpdate, TagResponse
from schemas.base_response import BaseResponse
from services.tag_service import get_tag_service   

router = APIRouter(
    prefix="/tags",
   tags=["tags"]
)

@router.post("/", response_model=BaseResponse[TagResponse] | TagResponse)
async def create_tag(
    tag: TagCreate,
    service=Depends(get_tag_service)
):
    db_tag = await service.create_tag(tag)
    if db_tag is None:
        raise HTTPException(status_code=400, detail="Tag creation failed")
    return BaseResponse(
        message="Tag created successfully",
        status="success",
        data=db_tag,
    )

@router.get("/{id}", response_model=BaseResponse[TagResponse] | TagResponse)
async def get_tag(
    id: PydanticObjectId,
    service=Depends(get_tag_service)
):
    db_tag = await service.get_tag(id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return BaseResponse(
        message="Tag retrieved successfully",
        status="success",
        data=db_tag
    )

@router.get("/", response_model=BaseResponse[list[TagResponse]] | list[TagResponse])
async def get_all_tags(
    service=Depends(get_tag_service)
):
    db_tags = await service.get_all_tags()
    return BaseResponse(
        message="Tags retrieved successfully",
        status="success",
        data=db_tags
    )

@router.put("/{id}", response_model=BaseResponse[TagResponse] | TagResponse)
async def update_tag(   
    id: PydanticObjectId, 
    tag: TagUpdate,
    service=Depends(get_tag_service)
):
    db_tag = await service.update_tag(id, tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return BaseResponse(
        message="Tag updated successfully",
        status="success",
        data=db_tag
    )

@router.delete("/{id}", response_model=BaseResponse[TagResponse] | TagResponse)
async def delete_tag(id: PydanticObjectId, service=Depends(get_tag_service)):
    db_tag = await service.delete_tag(id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return BaseResponse(
        message="Tag deleted successfully",
        status="success",
        data=db_tag
    )