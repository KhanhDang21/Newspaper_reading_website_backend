from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from schemas.user_info_post_schema import UserInfoPostCreate, UserInfoPostResponse
from schemas.base_response import BaseResponse
from services.user_info_post_service import get_user_info_post_service
from configs.authentication import get_current_user

router = APIRouter(
    prefix="/user_info_posts",
    tags=["user-info-posts"]
)

@router.post("/", response_model=BaseResponse[UserInfoPostResponse] | UserInfoPostResponse)
async def create_user_info_post(
    user_info_post_create: UserInfoPostCreate,
    service= Depends(get_user_info_post_service),
    current_user= Depends(get_current_user)
):
    user_info_post = await service.create_user_info_post(user_info_post_create, current_user)
    if not user_info_post:
        raise HTTPException(status_code=400, detail="Error creating user info post")
    return BaseResponse(
        message="User info post created successfully",
        status="success",
        data=user_info_post
    )

@router.delete("/{id}", response_model=BaseResponse[UserInfoPostResponse] | UserInfoPostResponse)
async def delete_user_info_post(
    id: PydanticObjectId,
    service= Depends(get_user_info_post_service),
    current_user= Depends(get_current_user)
):
    user_info_post = await service.delete_user_info_post(id, current_user)
    if not user_info_post:
        return BaseResponse(
            message="User info post not found or you are not allowed to delete",
            status="error",
            data=None
        )
    return BaseResponse(
        message="User info post deleted successfully",
        status="success",
        data=user_info_post
    )

@router.get("/", response_model=BaseResponse[list[UserInfoPostResponse]])
async def get_post_by_user_info(
    service= Depends(get_user_info_post_service),
    current_user= Depends(get_current_user)
):
    user_info_posts = await service.get_post_by_user_info(current_user)
    return BaseResponse(
        message="User info posts retrieved successfully",
        status="success",
        data=user_info_posts
    )