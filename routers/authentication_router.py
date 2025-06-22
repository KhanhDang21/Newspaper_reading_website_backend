from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from services.authentication_service import get_authen_service
from configs.authentication import get_current_user
from schemas.authentication_schema import UserPasswordUpdate, UserAuthentication


router = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)


@router.post("/register")
async def register_user(
    user: UserAuthentication,
    authen_service=Depends(get_authen_service),
):
    return await authen_service.register_user(user)


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authen_service=Depends(get_authen_service),
):
    return await authen_service.authenticate_user(form_data)


@router.put("/update-password")
async def update_password(
    request: UserPasswordUpdate,
    authen_service=Depends(get_authen_service),
    user=Depends(get_current_user),
):
    try:
        return await authen_service.update_password(request, user.username)
    except Exception as e:
        print(e)
        raise e
