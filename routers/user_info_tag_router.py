from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from schemas.user_info_tag_schema import UserInfoTagCreate, UserInfoTagResponse
from schemas.base_response import BaseResponse
from services.user_info_tag_service import get_user_info_tag_service
from configs.authentication import get_current_user

router = APIRouter(
    prefix="/user-info-tags",
    tags=["user-info-tags"]
)

@router.post("/", response_model=BaseResponse[UserInfoTagResponse] | UserInfoTagResponse)
async def create_user_info_tag(
    user_info_tag: UserInfoTagCreate,
    service=Depends(get_user_info_tag_service),
    current_user=Depends(get_current_user)
):
    db_user_info_tag = await service.create_user_info_tag(user_info_tag, current_user)
    
    if db_user_info_tag is None:
        raise HTTPException(status_code=400, detail="User info tag creation failed")
    return BaseResponse(
        message="User info tag created successfully",
        status="success",
        data=db_user_info_tag,
    )


@router.get("/{id}", response_model=BaseResponse[UserInfoTagResponse] | UserInfoTagResponse)
async def get_user_info_tag(
    id: PydanticObjectId,
    service=Depends(get_user_info_tag_service)
):
    db_user_info_tag = await service.get_user_info_tag(id)
    if db_user_info_tag is None:
        raise HTTPException(status_code=404, detail="User info tag not found")
    return BaseResponse(
        message="User info tag retrieved successfully",
        status="success",
        data=db_user_info_tag
    )

@router.get("/", response_model=BaseResponse[list[UserInfoTagResponse]] | list[UserInfoTagResponse])
async def get_all_user_info_tags(
    service=Depends(get_user_info_tag_service),
    current_user=Depends(get_current_user)
):
    db_user_info_tags = await service.get_all_tags_by_user_info(current_user)
    return BaseResponse(
        message="User info tags retrieved successfully",
        status="success",
        data=db_user_info_tags
    )


@router.delete("/{id}", response_model=BaseResponse[UserInfoTagResponse] | UserInfoTagResponse)
async def delete_user_info_tag(
    id: PydanticObjectId,
    service=Depends(get_user_info_tag_service),
    current_user=Depends(get_current_user)
):
    db_user_info_tag = await service.delete_user_info_tag(id, current_user)
    if db_user_info_tag is None:
        raise HTTPException(status_code=404, detail="User info tag not found")
    return BaseResponse(
        message="User info tag deleted successfully",
        status="success",
        data=db_user_info_tag
    )



