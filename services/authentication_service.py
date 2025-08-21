from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from configs.authentication import (
    verify_password,
    hash_password,
    create_access_token,
)
from schemas.authentication_schema import Token, UserPasswordUpdate
from schemas.base_response import BaseResponse
from datetime import timedelta
from models.user_authentication_model import UserAuthentication
#from schemas.authentication_schema import UserAuthentication as UserAuthenticationSchema
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRED_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRED_MINUTES")


def get_authen_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    async def register_user(self, user: UserAuthentication) -> BaseResponse:
        try:
            existing_user = await UserAuthentication.find_one({"username": user.username})

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists!"
                )

            new_user = UserAuthentication(
                username=user.username,
                hashed_password=hash_password(user.password),
            )
            await new_user.insert()

            return BaseResponse(message="User registered successfully!")
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while registering the user!"
            )


    async def authenticate_user(
        self, form_data: OAuth2PasswordRequestForm
    ) -> Token | HTTPException:
    
        user = await UserAuthentication.find_one(
            {
                "username": form_data.username
            }
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot validate user!",
            )
        
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot validate user!",
            )

        user_id = str(user.id)

        user_info_fetched = await user.user_info.fetch()
        user_info_id = str(user_info_fetched.id) if user_info_fetched else None

        access_token = create_access_token(
            {
                "sub": user.username,
                "id": user_id,
                "user_info_id": user_info_id
            },
            timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES)),
        )
        

        return Token(access_token=access_token, token_type="bearer")

    
    async def update_password(
        self,
        request: UserPasswordUpdate,
        username: str
    ) -> BaseResponse:
        try:
            user_model = await UserAuthentication.find_one(
                {"username": username}
            )

            if not user_model:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found!"
                )

            is_valid_password = verify_password(
                request.current_password, user_model.hashed_password
            )

            if not is_valid_password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Current password is incorrect!"
                )

            user_model.hashed_password = hash_password(request.new_password)
            await user_model.save()

            return BaseResponse(message="Password updated!")
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the password!"
            )
