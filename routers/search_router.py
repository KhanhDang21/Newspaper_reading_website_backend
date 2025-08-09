from fastapi import APIRouter, Depends, Query
from typing import List
from configs.redis import redis_client
from models.post_model import Post
from configs.authentication import get_current_user

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

MAX_HISTORY = 10

@router.get("/", summary="Search posts by title")
async def search(
    q: str = Query(...),
    current_user = Depends(get_current_user)
):
    key = f"search_history:{current_user.id}"
    
    redis_client.lpush(key, q)
    redis_client.ltrim(key, 0, MAX_HISTORY - 1)

    results = await Post.find({
        "title": {"$regex": q, "$options": "i"}  
    }).to_list()

    return {"query": q, "results": results}
    

@router.get("/history", response_model=List[str])
async def get_history(
    current_user = Depends(get_current_user)
):
    key = f"search_history:{current_user.id}"
    return redis_client.lrange(key, 0, -1)
