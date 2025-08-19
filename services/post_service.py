from beanie import PydanticObjectId
from models.post_model import Post
from models.post_tag_model import PostTag
from models.newspaper_publisher_model import NewspaperPublisher
from schemas.post_schema import PostCreate, PostUpdate, PostResponse
from bson import ObjectId

class PostServiceFactory:
    @staticmethod
    def create_service():
        return PostService()


class PostService:
    async def create_post(self, request: PostCreate) -> PostResponse:
        try:
            post = Post(**request.dict())
            await post.insert()
            
            publisher = await NewspaperPublisher.find_one(NewspaperPublisher.domain == request.domain)

            if publisher:
                post.newspaper_publisher = publisher
                await post.save()
            else:
                post.newspaper_publisher = None
                await post.save()

            post.newspaper_publisher = publisher

            await post.save()

            return PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                summary=post.summary,
                domain=post.domain,
                image_URL=post.image_URL,
                highlight=post.highlight,
                references=post.references,
                author=post.author,
                timestamp=post.timestamp,
                topic=post.topic,
                newspaper_publisher=post.newspaper_publisher.id if post.newspaper_publisher else None
            )
        except Exception as e:
            print(e)
            return None
        

    async def get_post(self, id: PydanticObjectId) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
                
            newspaper_publisher = await post.newspaper_publisher.fetch()

            return PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                summary=post.summary,
                domain=post.domain,
                image_URL=post.image_URL,
                highlight=post.highlight,
                references=post.references,
                author=post.author,
                timestamp=post.timestamp,
                topic=post.topic,
                newspaper_publisher=newspaper_publisher.id if newspaper_publisher else None
            )
        
        except Exception as e:
            print(e)
            return None
    

    async def get_all_posts(self) -> list[PostResponse]:
        try:
            db_post = await Post.find_all().sort(-Post.id).to_list()

            results = []
            for post in db_post:
                publisher_id = None
                if post.newspaper_publisher is not None:
                    publisher = await post.newspaper_publisher.fetch()
                    publisher_id = publisher.id

                results.append(
                    PostResponse(
                        id=post.id,
                        title=post.title,
                        content=post.content,
                        summary=post.summary,
                        domain=post.domain,
                        image_URL=post.image_URL,
                        highlight=post.highlight,
                        references=post.references,
                        author=post.author,
                        timestamp=post.timestamp,
                        topic=post.topic,
                        newspaper_publisher=publisher_id
                    )
                )
            return results
        except Exception as e:
            print(e)
            return []


    async def update_post(self, id: PydanticObjectId, request: PostUpdate) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(post, key, value)
            await post.save()

            if request.domain:
                publisher = await NewspaperPublisher.find_one(NewspaperPublisher.domain == request.domain)
                if publisher:
                    post.newspaper_publisher = publisher
                else:
                    post.newspaper_publisher = None
                await post.save()

            return PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                summary=post.summary,
                domain=post.domain,
                image_URL=post.image_URL,
                highlight=post.highlight,
                references=post.references,
                author=post.author,
                timestamp=post.timestamp,
                topic=post.topic,
                newspaper_publisher=post.newspaper_publisher.id if post.newspaper_publisher else None
            )
        except Exception as e:
            print(e)
            return None


    async def delete_post(self, id: PydanticObjectId) -> PostResponse:
        try:
            post = await Post.get(id)
            if not post:
                raise Exception("Post not found")
            await post.delete()

            newspaper_publisher = await post.newspaper_publisher.fetch() 

            return PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                summary=post.summary,
                domain=post.domain,
                image_URL=post.image_URL,
                highlight=post.highlight,
                references=post.references,
                author=post.author,
                timestamp=post.timestamp,
                topic=post.topic,
                newspaper_publisher=newspaper_publisher.id if newspaper_publisher else None
            )
        except Exception as e:
            print(e)
            return None
        
    
    async def get_posts_by_tag(self, tag_id: PydanticObjectId) -> list[PostResponse]:
        try:
            post_tags = await PostTag.find(PostTag.tag.id == tag_id).sort(-PostTag.id).to_list()
        
            results = []
            for post_item in post_tags:
                
                post = await post_item.post.fetch()
                
                publisher = await post.newspaper_publisher.fetch()
                publisher_id = publisher.id if publisher else None

                results.append(
                    PostResponse(
                        id=post.id,
                        title=post.title,
                        content=post.content,
                        summary=post.summary,
                        domain=post.domain,
                        image_URL=post.image_URL,
                        highlight=post.highlight,
                        references=post.references,
                        author=post.author,
                        timestamp=post.timestamp,
                        topic=post.topic,
                        newspaper_publisher=publisher_id
                    )
                )
            return results

        except Exception as e:
            print(f"[get_posts_by_tag] Error: {e}")
            return []


def get_post_service():
    try:
        yield PostServiceFactory.create_service()
    finally:
        pass

