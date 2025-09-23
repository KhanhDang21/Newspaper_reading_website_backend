from services.post_service import PostService
from schemas.post_schema import PostCreate

def filter_post_data(article: dict) -> dict:
    """Chỉ lấy các field có trong PostCreate"""
    return {
        "title": article.get("title", ""),
        "content": article.get("content", ""),
        "summary": article.get("summary", ""),
        "domain": article.get("domain", ""),
        "url": article.get("url", ""),
        "images": article.get("images", []),
        "highlight": article.get("highlight", ""),
        "references": article.get("references", []),
        "author": article.get("author", ""),
        "time": article.get("time", ""),
        "topic": article.get("topic", []),
    }

async def save_crawled_article(article: dict):
    """Lưu 1 bài viết crawl được vào DB"""
    service = PostService()
    request = PostCreate(**filter_post_data(article))
    return await service.create_post(request)
