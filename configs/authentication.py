from datetime import datetime, timedelta, timezone
from beanie import PydanticObjectId
from passlib.context import CryptContext
from jose import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from models.user_authentication_model import UserAuthentication
from models.user_info_model import UserInfo

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/authentication/token")


def hash_password(plain_password):
    return bcrypt_context.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expired_delta: timedelta):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + expired_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_bearer),
) -> UserAuthentication | HTTPException:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        user_info_id: str = payload.get("user_info_id")

        if user_id is None or username is None:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot validate user!",
            )

        user = await UserInfo.find_one(
            UserInfo.id == PydanticObjectId(user_info_id)
        )
        
        if not user:
            user = await UserAuthentication.find_one(
                UserAuthentication.id == PydanticObjectId(user_id)
            )

        return user
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot validate user!",
        )
