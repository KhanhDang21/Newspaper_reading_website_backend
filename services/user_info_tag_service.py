from models import user_info_tag_model
from models.user_info_tag_model import UserInfoTag
from schemas.user_info_tag_schema import UserInfoTagCreate, UserInfoTagResponse
from beanie import PydanticObjectId
from models.user_authentication_model import UserAuthentication
from models.tag_model import Tag

class UserInfoTagFactory:
    @staticmethod
    def create_service():
        return UserInfoTagService()


class UserInfoTagService:
    async def create_user_info_tag(self, user_info_tag: UserInfoTagCreate, current_user_id: PydanticObjectId) -> UserInfoTagResponse:
        try:

            tag = await Tag.find_one({"_id": user_info_tag.tag_id})

            if not tag:
                raise Exception("Tag not found")
            
            user_info_tag_model = UserInfoTag(
                user=current_user_id,
                tag=user_info_tag.tag_id
            )

            await user_info_tag_model.insert()

            fetched_user = await user_info_tag_model.user.fetch()
            fetched_tag = await user_info_tag_model.tag.fetch()

            return UserInfoTagResponse(
                id=user_info_tag_model.id,
                user_id=fetched_user.id,
                tag_id=fetched_tag.id
            )
        
        except Exception as e:
            print(e)
            return None
        
    
    async def get_user_info_tag(self, id: PydanticObjectId) -> UserInfoTagResponse:
        try:
            user_info_tag = await UserInfoTag.get(id)

            if not user_info_tag:
                raise Exception("User Info Tag not found")
            
            # Fetching user and tag details
            fetched_user = await user_info_tag.user.fetch()
            fetched_tag = await user_info_tag.tag.fetch()

            return UserInfoTagResponse(
                id=user_info_tag.id,
                user_id=fetched_user.id,
                tag_id=fetched_tag.id
            )
        except Exception as e:
            print(e)
            return None
        
    
    async def get_all_user_info_tags(self) -> list[UserInfoTagResponse]:
        try:
            user_info_tags = await UserInfoTag.find_all().to_list()

            response = []

            for tag in user_info_tags:
                fetched_user = await tag.user.fetch()  
                fetched_tag = await tag.tag.fetch()    

                response.append(UserInfoTagResponse(
                    id=tag.id,
                    user_id=fetched_user.id,
                    tag_id=fetched_tag.id
                ))
                
            return response

        except Exception as e:
            print("[get_all_user_info_tags error]:", e)
            return []


    async def update_user_info_tag(
        self, id: PydanticObjectId, user_info_tag: UserInfoTagCreate
    ) -> UserInfoTagResponse:
        try:
            existing_tag = await UserInfoTag.get(id)
            if not existing_tag:
                raise Exception("User Info Tag not found")
            for key, value in user_info_tag.dict(exclude_unset=True).items():
                setattr(existing_tag, key, value)
            await existing_tag.save()
            return UserInfoTagResponse(**existing_tag.dict())
        except Exception as e:
            print(e)
            return None


    async def delete_user_info_tag(self, id: PydanticObjectId) -> bool:
        try:
            user_info_tag = await UserInfoTag.get(id)
            if not user_info_tag:
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