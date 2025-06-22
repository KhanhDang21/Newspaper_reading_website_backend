from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from services.post_service import PostServiceFactory
from schemas.post_schema import PostCreate, PostUpdate, PostResponse
from schemas.base_response import BaseResponse
from services.post_service import get_post_service

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/", response_model=BaseResponse[PostResponse] | PostResponse)
async def create_post(
    post: PostCreate,
    sevice =  Depends(get_post_service)
):
    db_post = await sevice.create_post(post)
    if db_post is None:
        raise HTTPException(status_code=400, detail="Post creation failed")
    return BaseResponse(
        message="Post created successfully",
        status= "success",
        data=db_post,
    )

@router.get("/{id}", response_model=BaseResponse[PostResponse] | PostResponse)
async def get_post(
    id: PydanticObjectId,
    service = Depends(get_post_service)
):
    db_post = await service.get_post(id)
    return BaseResponse(
        message="Post retrieved successfully",
        status="success",
        data=db_post
    )

@router.get("/", response_model=BaseResponse[list[PostResponse]] | list[PostResponse])
async def get_all_posts(
    service=Depends(get_post_service)
):
    db_post = await service.get_all_posts()
    return BaseResponse(
        message="Posts retrieved successfully",
        status="success",
        data=db_post
    )

@router.put("/{id}", response_model=BaseResponse[PostResponse] | PostResponse)
async def update_post(
    id: PydanticObjectId, 
    post: PostUpdate,
    service=Depends(get_post_service)
):
    db_post = await service.update_post(id, post)
    return BaseResponse(
        message="Post updated successfully",
        status="success",
        data=db_post
    )

@router.delete("/{id}", response_model=BaseResponse[PostResponse] | PostResponse)
async def delete_post(id: PydanticObjectId, service=Depends(get_post_service)):
    db_post = await service.delete_post(id)
    return BaseResponse(
        message="Post deleted successfully",
        status="success",
        data=db_post
    )