from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from schemas.post_tag_schema import PostTagCreate, PostTagResponse, PostTagUpdate
from schemas.base_response import BaseResponse  
from services.post_tag_service import PostTagFactory, get_post_tag_service

router = APIRouter(
    prefix="/post-tag",
    tags=["post-tag"]
)


@router.post("/", response_model=BaseResponse[PostTagResponse] | PostTagResponse)
async def create_post_tag(
    post_tag: PostTagCreate,
    service=Depends(get_post_tag_service)
):
    db_post_tag = await service.create_post_tag(post_tag)
    if db_post_tag is None:
        raise HTTPException(status_code=400, detail="Post tag creation failed")
    return BaseResponse(
        message="Post tag created successfully",
        status="success",
        data=db_post_tag,
    )


@router.get("/{id}", response_model=BaseResponse[PostTagResponse] | PostTagResponse)
async def get_post_tag(
    id: PydanticObjectId,
    service=Depends(get_post_tag_service)
):
    db_post_tag = await service.get_post_tag(id)
    if db_post_tag is None:
        raise HTTPException(status_code=404, detail="Post tag not found")
    return BaseResponse(
        message="Post tag retrieved successfully",
        status="success",
        data=db_post_tag,
    )


@router.get("/", response_model=BaseResponse[list[PostTagResponse]] | list[PostTagResponse])
async def get_all_post_tags(
    service=Depends(get_post_tag_service)
):
    db_post_tags = await service.get_all_post_tags()
    return BaseResponse(
        message="Post tags retrieved successfully",
        status="success",
        data=db_post_tags,
    )


@router.put("/{id}", response_model=BaseResponse[PostTagResponse] | PostTagResponse)
async def update_post_tag(
    id: PydanticObjectId,
    post_tag: PostTagUpdate,
    service=Depends(get_post_tag_service)
):
    db_post_tag = await service.update_post_tag(id, post_tag)
    if db_post_tag is None:
        raise HTTPException(status_code=404, detail="Post tag not found")
    return BaseResponse(
        message="Post tag updated successfully",
        status="success",
        data=db_post_tag,
    )


@router.delete("/{id}", response_model=BaseResponse[PostTagResponse] | PostTagResponse)
async def delete_post_tag(
    id: PydanticObjectId,
    service=Depends(get_post_tag_service)
):
    db_post_tag = await service.delete_post_tag(id)
    if db_post_tag is None:
        raise HTTPException(status_code=404, detail="Post tag not found")
    return BaseResponse(
        message="Post tag deleted successfully",
        status="success",
        data=db_post_tag,
    )