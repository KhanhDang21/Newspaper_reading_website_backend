from models.user_info_tag_model import UserInfoTag
from schemas.user_info_tag_schema import UserInfoTagCreate, UserInfoTagResponse
from beanie import PydanticObjectId
from models.tag_model import Tag
from configs.authentication import get_current_user


class UserInfoTagFactory:
    @staticmethod
    def create_service():
        return UserInfoTagService()


class UserInfoTagService:
    async def create_user_info_tag(self, user_info_tag: UserInfoTagCreate, current_user: get_current_user) -> UserInfoTagResponse:
        try:

            tag = await Tag.find_one({"_id": user_info_tag.tag})

            if not tag:
                raise Exception("Tag not found")
            
            user_info_tag_model = UserInfoTag(
                user_info=current_user.id,
                tag=user_info_tag.tag
            )

            await user_info_tag_model.insert()

            fetched_user = await user_info_tag_model.user_info.fetch()
            fetched_tag = await user_info_tag_model.tag.fetch()

            return UserInfoTagResponse(
                id=user_info_tag_model.id,
                user_info=fetched_user.id,
                tag=fetched_tag.id
            )
        
        except Exception as e:
            print(e)
            return None
        
    
    async def get_user_info_tag(self, id: PydanticObjectId) -> UserInfoTagResponse:
        try:
            user_info_tag = await UserInfoTag.get(id)

            if not user_info_tag:
                raise Exception("User Info Tag not found")
            
            fetched_user = await user_info_tag.user_info.fetch()
            fetched_tag = await user_info_tag.tag.fetch()

            return UserInfoTagResponse(
                id=user_info_tag.id,
                user_info=fetched_user.id,
                tag=fetched_tag.id
            )
        except Exception as e:
            print(e)
            return None
        
    
    async def get_all_tags_by_user_info(self, current_user: get_current_user) -> list[UserInfoTagResponse]:
        try:
            user_info_tags = await UserInfoTag.find(UserInfoTag.user_info.id == current_user.id).to_list()

            response = []

            for tag in user_info_tags:
                fetched_user = await tag.user_info.fetch()
                fetched_tag = await tag.tag.fetch()

                response.append(UserInfoTagResponse(
                    id=tag.id,
                    user_info=fetched_user.id,
                    tag=fetched_tag.id
                ))
                
            return response

        except Exception as e:
            print("[get_all_user_info_tags error]:", e)
            return []


    async def delete_user_info_tag(self, id: PydanticObjectId, current_user: get_current_user) -> bool:
        try:
            user_info_tag = await UserInfoTag.get(id)

            user_info_fetched = await user_info_tag.user_info.fetch()

            if not user_info_tag or user_info_fetched.id != current_user.id:
                raise Exception("User Info Tag not found")
            await user_info_tag.delete()
            return True
        except Exception as e:
            print(e)
            return False    
    

def get_user_info_tag_service():
    try:
        yield UserInfoTagFactory.create_service()
    finally:
        pass