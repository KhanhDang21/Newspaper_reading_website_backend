from beanie import PydanticObjectId
from models.comment_model import Comment
from schemas.comment_schema import CommentCreate, CommentUpdate, CommentResponse
from configs.authentication import get_current_user


class CommentServiceFactory:
    @staticmethod
    def get_comment_service():
        return CommentService()
    
class CommentService:
    async def create_comment(self, comment_create: CommentCreate, current_user: get_current_user) -> CommentResponse:
        try:
            comment = Comment(**comment_create.dict(), user_info=current_user.id)
            await comment.insert()

            post_fetched = await comment.post.fetch()
            user_info_fetched = await comment.user_info.fetch()

            return CommentResponse(
                id=comment.id,
                post=post_fetched.id,
                user_info=user_info_fetched.id,
                content=comment.content
            )
        except Exception as e:
            print(e)
            return None

    async def update_comment(self, comment_id: PydanticObjectId, comment_update: CommentUpdate, current_user: get_current_user) -> CommentResponse:
        try:
            comment = await Comment.get(comment_id)

            user_info_fetched = await comment.user_info.fetch()

            if not comment or user_info_fetched.id != current_user.id:
                return None

            comment.content = comment_update.content
            await comment.save()

            post_fetched = await comment.post.fetch()
            user_info_fetched = await comment.user_info.fetch()

            return CommentResponse(
                id=comment.id,
                post=post_fetched.id,
                user_info=user_info_fetched.id,
                content=comment.content
            )
        except Exception as e:
            print(e)
            return None

    async def delete_comment(self, comment_id: PydanticObjectId, current_user: get_current_user) -> bool:
        try:
            comment = await Comment.get(comment_id)

            user_info_fetched = await comment.user_info.fetch()

            if not comment or user_info_fetched.id != current_user.id:
                return False

            await comment.delete()
            return True
        except Exception as e:
            print(e)
            return False


    async def get_all_comments_by_post(self, post_id: PydanticObjectId) -> list[CommentResponse]:
        try:
            comments = await Comment.find(Comment.post.id == post_id).sort(-Comment.id).to_list()

            result = []
            for comment in comments:
                post_fetched = await comment.post.fetch()
                user_info_fetched = await comment.user_info.fetch()
                result.append(
                    CommentResponse(
                        id=comment.id,
                        post=post_fetched.id,
                        user_info=user_info_fetched.id,
                        content=comment.content
                    )
                )

            return result
        except Exception as e:
            print(e)
            return []


def get_comment_service():
    try:
        yield CommentServiceFactory.get_comment_service()
    finally:
        pass
