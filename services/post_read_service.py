from configs.redis import redis_client
from configs.authentication import get_current_user
from beanie import PydanticObjectId

class PostReadFactory:
    @staticmethod
    def create_service():
        return PostReadService()
    
class PostReadService:
    def mark_post_as_read(self, post_id: PydanticObjectId, current_user: get_current_user):
        try:
            user_id = str(current_user.id)
            key = f"user:{user_id}:read_posts"

            redis_client.sadd(key, str(post_id))

            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_all_read_posts(self, current_user: get_current_user):
        try:
            user_id = str(current_user.id)
            key = f"user:{user_id}:read_posts"

            read_posts = redis_client.smembers(key)
            return {"status": "success", "data": list(read_posts)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

def get_post_read_service():
    try:
        yield PostReadFactory.create_service()
    finally:
        pass