from beanie import PydanticObjectId
from models.post_model import Post
from schemas.post_schema import PostCreate, PostUpdate, PostResponse


class PostServiceFactory:
    @staticmethod
    def create_service():
        return PostService()


class PostService:
    async def create_post(self, request: PostCreate) -> PostResponse:
        try:
            post = Post(**request.dict())
            await post.insert()
            return PostResponse(**post.dict())
        except Exception as e:
            print(e)
            return None
        

    async def get_post(self, id: PydanticObjectId) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
            return PostResponse(**post.dict())
        except Exception as e:
            print(e)
            return None
    

    async def get_all_posts(self) -> list[PostResponse]:
        try:
            return await Post.find_all().to_list()
        except Exception as e:
            print(e)
            return None


    async def update_post(self, id: PydanticObjectId, request: PostUpdate) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(post, key, value)
            await post.save()
            return PostResponse(**post.dict())
        except Exception as e:
            print(e)
            return None


    async def delete_post(self, id: PydanticObjectId) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
            await post.delete()
            return PostResponse(**post.dict())
        except Exception as e:
            print(e)
            return None


def get_post_service():
    try:
        yield PostServiceFactory.create_service()
    finally:
        pass

