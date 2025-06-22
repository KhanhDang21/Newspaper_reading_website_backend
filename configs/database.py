from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

from models.user_info_model import UserInfo
from models.post_model import Post
from models.product_solution_model import ProductSolution
from models.user_authentication_model import UserAuthentication

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)

async def init_db():
    try:
        await client.admin.command('ping')
        print("✅ MongoDB connection successful")
        
        await init_beanie(
            database=client[DB_NAME],
            document_models=[
                UserInfo,
                ProductSolution,
                Post,
                UserAuthentication  
            ]
        )
        print("✅ Beanie initialized successfully")
        
    except PyMongoError as e:
        print(f"❌ MongoDB connection error: {e}")
        raise
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        raise
