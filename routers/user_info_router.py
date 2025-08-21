from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from services.user_info_service import get_userinfo_service
from schemas.user_info_schema import UserInfoResponse, UserInfoCreate, UserInfoUpdate
from schemas.base_response import BaseResponse
from configs.authentication import get_current_user


router = APIRouter(
    prefix="/user-info", 
    tags=["user-info"]
    )


@router.post("/", response_model=BaseResponse[UserInfoResponse] | UserInfoResponse)
async def create_user(
    request: UserInfoCreate,
    service = Depends(get_userinfo_service),
    current_user = Depends(get_current_user)
):
    user_db = await service.create_user(request, current_user)
    return BaseResponse(
        message="User created successfully",
        status="success",
        data=user_db
    )


@router.get("/{id}", response_model=BaseResponse[UserInfoResponse] | UserInfoResponse)
async def get_user(
    id: PydanticObjectId,
    service = Depends(get_userinfo_service)
):
    user_db = await service.get_user(id)
    return BaseResponse(
        message="User retrieved successfully",
        status="success",
        data=user_db
    )


@router.put("/{id}", response_model=BaseResponse[UserInfoResponse] | UserInfoResponse)
async def update_user(
    id: PydanticObjectId, 
    request: UserInfoUpdate,
    service = Depends(get_userinfo_service),
    current_user = Depends(get_current_user)
):
    user_db = await service.update_user(id, request, current_user)
    return BaseResponse(
        message="User updated successfully",
        status="success",
        data=user_db
    )
