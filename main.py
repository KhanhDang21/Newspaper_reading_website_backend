from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination, Params
from configs.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
from ai_crawl import AutoNewsCrawler
from adapter import save_crawled_article
import asyncio
import logging
from routers.user_info_router import router as userinfo_router
from routers.newspaper_publisher_router import router as newspaper_published_router
from routers.post_router import router as post_router
from routers.authentication_router import router as auth_router
from routers.tag_router import router as tag_router
from routers.user_info_tag_router import router as user_info_tag_router
from routers.search_router import router as search_router
from routers.post_tag_router import router as post_tag_router
from routers.comment_router import router as comment_router
from routers.user_info_post_router import router as user_info_post_router
from routers.post_read_router import router as post_read_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("✅ Database đã sẵn sàng")

    asyncio.create_task(start_crawler_loop())
    yield

app = FastAPI(lifespan=lifespan)

crawler = AutoNewsCrawler()

logger = logging.getLogger("crawler")
logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def start_crawler_loop():
    logger.info("🚀 Background crawler started")
    crawler = AutoNewsCrawler()
    while True:
        try:
            articles = await asyncio.to_thread(crawler.crawl_multiple_urls)
            logger.info(f"📑 Crawl được {len(articles)} bài viết")
            for art in articles:
                try:
                    await save_crawled_article(art)
                    logger.info(f"✅ Lưu bài viết: {art.get('title', 'N/A')}")
                except Exception as e:
                    logger.exception("❌ Lỗi khi lưu bài viết: %s", e)
            await asyncio.sleep(120)
        except Exception as e:
            logger.exception("❌ Lỗi vòng lặp crawler: %s", e)
            await asyncio.sleep(10)


app.include_router(auth_router, prefix="/api")
app.include_router(userinfo_router, prefix="/api")
app.include_router(post_router, prefix="/api")
app.include_router(newspaper_published_router, prefix="/api")
app.include_router(tag_router, prefix="/api")
app.include_router(user_info_tag_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(post_tag_router, prefix="/api")
app.include_router(comment_router, prefix="/api")
app.include_router(user_info_post_router, prefix="/api")
app.include_router(post_read_router, prefix="/api")

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)