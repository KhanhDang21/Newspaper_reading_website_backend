from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from schemas.comment_schema import CommentCreate, CommentUpdate, CommentResponse
from schemas.base_response import BaseResponse
from services.comment_service import get_comment_service
from configs.authentication import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.post("/", response_model=BaseResponse[CommentResponse] | CommentResponse)
async def create_comment(comment_create: CommentCreate,
                         service=Depends(get_comment_service),
                         current_user=Depends(get_current_user)):
    db_comment = await service.create_comment(comment_create, current_user)
    if not db_comment:
        raise HTTPException(status_code=400, detail="Error creating comment")
    return BaseResponse(
        message="Comment created successfully",
        status="success",
        data=db_comment
    )


@router.get("/{post_id}", response_model=BaseResponse[list[CommentResponse]])
async def get_all_comments_by_post(
    post_id: PydanticObjectId,
    service=Depends(get_comment_service)
):
    db_comments = await service.get_all_comments_by_post(post_id)
    return BaseResponse(
        message="Comments retrieved successfully",
        status="success",
        data=db_comments
    )

@router.put("/{comment_id}", response_model=BaseResponse[CommentResponse] | CommentResponse)
async def update_comment(comment_id: PydanticObjectId,
                          comment_update: CommentUpdate,
                          service=Depends(get_comment_service),
                          current_user=Depends(get_current_user)):
    db_comment = await service.update_comment(comment_id, comment_update, current_user)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    return BaseResponse(
        message="Comment updated successfully",
        status="success",
        data=db_comment
    )


@router.delete("/{comment_id}", response_model=BaseResponse[bool])
async def delete_comment(comment_id: PydanticObjectId,
                          service=Depends(get_comment_service),
                          current_user=Depends(get_current_user)):
    is_deleted = await service.delete_comment(comment_id, current_user)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Comment not found or not authorized")
    return BaseResponse(
        message="Comment deleted successfully",
        status="success",
        data=is_deleted
    )
