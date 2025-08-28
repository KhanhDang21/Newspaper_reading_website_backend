from fastapi import APIRouter, Depends, Query, Request
from typing import List, Optional
from configs.redis import redis_client
from models.post_model import Post
from models.post_tag_model import PostTag
from configs.authentication import get_current_user
from beanie import PydanticObjectId
from fastapi import HTTPException

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

MAX_HISTORY = 10

async def get_optional_user(request: Request):
    try:
        return await get_current_user(request)
    except HTTPException:
        return None


@router.get("/", summary="Search posts by title")
async def search(
    q: str = Query(..., description="Từ khóa tìm kiếm"),
    tag_id: Optional[str] = Query(None, description="ID của tag cần lọc"),
    current_user = Depends(get_optional_user)
):

    if current_user:
        key = f"search_history:{current_user.id}"
        redis_client.lpush(key, q)
        redis_client.ltrim(key, 0, MAX_HISTORY - 1)
    
    post_ids = None
    if tag_id:
        post_tags = await PostTag.find(
            PostTag.tag_id == PydanticObjectId(tag_id)
        ).to_list()
        post_ids = [pt.post_id for pt in post_tags]

    filter_query = {"title": {"$regex": q, "$options": "i"}}
    if post_ids is not None:
        filter_query["_id"] = {"$in": post_ids}

    results = await Post.find(filter_query).to_list()

    return {"query": q, "results": results}


@router.get("/history", response_model=List[str])
async def get_history(
    current_user = Depends(get_current_user)
):
    
    if not current_user:
        return []

    key = f"search_history:{current_user.id}"
    return redis_client.lrange(key, 0, -1)
