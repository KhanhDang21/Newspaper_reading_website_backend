from beanie import PydanticObjectId
from schemas.user_info_post_schema import UserInfoPostCreate, UserInfoPostResponse
from models.user_info_post_model import UserInfoPost
from configs.authentication import get_current_user


class UserInfoPostFactory():
    @staticmethod
    def get_user_info_post_service():
        return UserInfoPostService()
    

class UserInfoPostService:
    async def create_user_info_post(self, user_info_post_create: UserInfoPostCreate, current_user: get_current_user) -> UserInfoPostResponse:
        try:
            user_info_post = UserInfoPost(
                **user_info_post_create.dict(),
                user_info =current_user.id
            )

            db_user_info_post = await UserInfoPost.find_one(UserInfoPost.post == user_info_post.post)

            if db_user_info_post:
                raise Exception("User info post already exists for this post")

            await user_info_post.insert()

            user_info_fetched = await user_info_post.user_info.fetch()
            post_fetched = await user_info_post.post.fetch()

            return UserInfoPostResponse(
                id=user_info_post.id,
                user_info=user_info_fetched.id,
                post=post_fetched.id
            )
        except Exception as e:
            print(e)
            return None

    async def delete_user_info_post(self, id: PydanticObjectId, current_user: get_current_user) -> UserInfoPostResponse:
        try:
            user_info_post = await UserInfoPost.get(id)
            
            if not user_info_post:
                return None

            user_info_fetched = await user_info_post.user_info.fetch()

            if user_info_fetched.id != current_user.id:
                return None

            await user_info_post.delete()
            return user_info_post
        except Exception as e:
            print(e)
            return None

    async def get_post_by_user_info(self, current_user: get_current_user) -> list[UserInfoPostResponse]:
        try:
            user_info_posts = await UserInfoPost.find(UserInfoPost.user_info.id == current_user.id).to_list()
            
            results = []

            for user_info_post in user_info_posts:
                user_info_fetched = await user_info_post.user_info.fetch()
                post_fetched = await user_info_post.post.fetch()

                results.append(UserInfoPostResponse(
                    id=user_info_post.id,
                    user_info=user_info_fetched.id,
                    post=post_fetched.id
                ))

            return results

        except Exception as e:
            print(e)
            return []

def get_user_info_post_service():
    try:
        return UserInfoPostFactory.get_user_info_post_service()
    finally:
        pass