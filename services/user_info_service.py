from beanie import PydanticObjectId
from models.user_info_model import UserInfo
from schemas.user_info_schema import UserInfoCreate, UserInfoUpdate, UserInfoResponse
from configs.authentication import get_current_user

class UserinfoServiceFactory:
    @staticmethod
    def create_service():
        return UserinfoService()
    

class UserinfoService:
    async def create_user(self, request: UserInfoCreate, current_user: get_current_user) -> UserInfoResponse:
        try:
            user_info = UserInfo(**request.dict())

            await user_info.insert()
            
            current_user.user_info = user_info

            await current_user.save()

            return UserInfoResponse(**user_info.dict())
        except Exception as e:
            print(e)
            return None
        

    async def get_user(self, id: PydanticObjectId) -> UserInfoResponse:
        try:
            user_info = await UserInfo.get(id)
            if not user_info:
                raise Exception("User not found")
            return UserInfoResponse(**user_info.dict())
        except Exception as e:
            print(e)
            return None


    async def update_user(self, id: PydanticObjectId, request: UserInfoUpdate, current_user: get_current_user) -> UserInfoResponse:
        try:
            user = await UserInfo.get(id)
            if not user:
                raise Exception("User not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(user, key, value)
            await user.save()

            current_user.user_info = user
            await current_user.save()

            return UserInfoResponse(**user.dict())
        except Exception as e:
            print(e)
            return None



def get_userinfo_service():
    try:
        yield UserinfoServiceFactory.create_service()
    finally:
        pass