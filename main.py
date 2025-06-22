from contextlib import asynccontextmanager
from fastapi import FastAPI
from configs.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from routers.user_info_router import router as userinfo_router
from routers.product_solution_router import router as solution_router
from routers.post_router import router as post_router
from routers.authentication_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api")
app.include_router(userinfo_router, prefix="/api")
app.include_router(post_router, prefix="/api")
app.include_router(solution_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)