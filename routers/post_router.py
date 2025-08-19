from fastapi import APIRouter, Depends, HTTPException, Query
from beanie import PydanticObjectId
from fastapi_pagination import Params, add_pagination, Page, paginate
from fastapi_pagination.customization import CustomizedPage, UseParams
from typing import TypeVar
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

T = TypeVar("T")

class MyParamsAllPost(Params):
    size: int = Query(10, ge=1, le=100, alias="pageSize")
    #page: int = Query(1, ge=1, alias="pageNumber")

CustomPageAllPost = CustomizedPage[
    Page[T],
    UseParams(MyParamsAllPost),
]

@router.get("/", response_model=CustomPageAllPost[PostResponse])
async def get_all_posts(
    service=Depends(get_post_service),
):
    db_post = await service.get_all_posts()
    return paginate(db_post)

add_pagination(router)


class MyParamsPostByTag(Params):
    size: int = Query(3, ge=1, le=100, alias="pageSize")
    #page: int = Query(1, ge=1, alias="pageNumber")

CustomPagePostByTag = CustomizedPage[
    Page[T],
    UseParams(MyParamsPostByTag),
]


@router.get("/by_tag/{tag_id}", response_model=CustomPagePostByTag[PostResponse])
async def get_posts_by_tag(
    tag_id: PydanticObjectId,
    service=Depends(get_post_service),
):
    db_posts = await service.get_posts_by_tag(tag_id)
    return paginate(db_posts)

add_pagination(router)


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