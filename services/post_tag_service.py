from beanie import PydanticObjectId
from pydantic import BaseModel
from models.post_tag_model import PostTag
from models.post_model import Post
from models.tag_model import Tag
from schemas.post_tag_schema import PostTagCreate, PostTagUpdate, PostTagResponse

class PostTagFactory:
    @staticmethod
    def create_service():
        return PostTagService()
    
class PostTagService:
    async def create_post_tag(self, request: PostTagCreate) -> PostTagResponse:
        try:
            post = await Post.get(request.post)
            tag = await Tag.get(request.tag)
            if not post or not tag:
                raise Exception("Post or Tag not found")
                
            post_tag = PostTag(**request.dict())
            
            await post_tag.insert()

            post_fetched = await post_tag.post.fetch()
            tag_fetched = await post_tag.tag.fetch()

            return PostTagResponse(
                id=post_tag.id,
                post=post_fetched.id,
                tag=tag_fetched.id
            )
        except Exception as e:
            print(e)
            return None

    async def get_post_tag(self, id: PydanticObjectId) -> PostTagResponse:
        try:
            post_tag = await PostTag.get(id)
            if not post_tag:
                raise Exception("PostTag not found")
            
            post_fetched = await post_tag.post.fetch()
            tag_fetched = await post_tag.tag.fetch()
            return PostTagResponse(
                id=post_tag.id,
                post=post_fetched.id,
                tag=tag_fetched.id
            )
        except Exception as e:
            print(e)
            return None

    async def get_all_post_tags(self) -> list[PostTagResponse]:
        try:
            post_tags = await PostTag.find_all().to_list()
            response = []

            for post_tag in post_tags:
                fetched_post = await post_tag.post.fetch()
                fetched_tag = await post_tag.tag.fetch()

                response.append(PostTagResponse(
                    id=post_tag.id,
                    post=fetched_post.id,
                    tag=fetched_tag.id
                ))  
                
            return response
        
        except Exception as e:
            print(e)
            return None

    async def update_post_tag(self, id: PydanticObjectId, request: PostTagUpdate) -> PostTagResponse:
        try:
            post_tag = await PostTag.get(id)
            if not post_tag:
                raise Exception("PostTag not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(post_tag, key, value)
            await post_tag.save()

            post_fetched = await post_tag.post.fetch()
            tag_fetched = await post_tag.tag.fetch()
            return PostTagResponse(
                id=post_tag.id,
                post=post_fetched.id,
                tag=tag_fetched.id
            )
        except Exception as e:
            print(e)
            return None
        
    async def delete_post_tag(self, id: PydanticObjectId) -> PostTagResponse:
        try:
            post_tag = await PostTag.get(id)
            if not post_tag:
                raise Exception("PostTag not found")
            await post_tag.delete()

            post_fetched = await post_tag.post.fetch()
            tag_fetched = await post_tag.tag.fetch()

            return PostTagResponse(
                id=post_tag.id,
                post=post_fetched.id,
                tag=tag_fetched.id
            )
        except Exception as e:
            print(e)
            return None

def get_post_tag_service():
    try:
        yield PostTagFactory.create_service()
    finally:
        pass