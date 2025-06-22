from beanie import PydanticObjectId
from models.user_info_model import UserInfo
from models.user_authentication_model import UserAuthentication
from schemas.user_info_schema import UserInfoCreate, UserInfoUpdate, UserInfoResponse

class UserinfoServiceFactory:
    @staticmethod
    def create_service():
        return UserinfoService()
    

class UserinfoService:
    async def create_user(self, request: UserInfoCreate, current_user: UserAuthentication) -> UserInfoResponse:
        try:
            user_info = UserInfo(
                user_id= current_user.id,
                full_name=request.full_name,
                number_phone=request.number_phone,
                email=request.email,
                id_personal=request.id_personal,
                role=request.role,
                status=request.status
            )
            await user_info.insert()
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
        

    async def get_all_users(self) -> list[UserInfoResponse]:
        try:
            return await UserInfo.find_all().to_list()
        except Exception as e:
            print(e)
            return None


    async def update_user(self, id: PydanticObjectId, request: UserInfoUpdate) -> UserInfoResponse:
        try:
            user = await UserInfo.get(id)
            if not user:
                raise Exception("User not found")
            for key, value in request.dict(exclude_unset=True).items():
                setattr(user, key, value)
            await user.save()
            return UserInfoResponse(**user.dict())
        except Exception as e:
            print(e)
            return None


    async def delete_user(self, id: PydanticObjectId) -> UserInfoResponse:
        try:
            user = await UserInfo.get(id)
            if not user:
                raise Exception("User not found")
            await user.delete()
            return UserInfoResponse(**user.dict())
        except Exception as e:
            print(e)
            return None


def get_userinfo_service():
    try:
        yield UserinfoServiceFactory.create_service()
    finally:
        pass