from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from .schemas import (
    UserCreateModel,
    UserLoginModel,
    AccessToken,
    UserModel,
    UserBookModel,
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from .service import UserService
from .utils import create_access_token, verify_password
from src.db.redis import add_jti_to_blocklist
from src.db.main import get_session

auth_router = APIRouter()

user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email already exists",
        )

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.get("/me", response_model=UserBookModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user(email, session)

    if user is not None and verify_password(password, user.password_hash):
        access_token = create_access_token(
            user_data={"email": user.email, "user_uid": str(user.uid)}
        )

        refresh_token = create_access_token(
            user_data={
                "email": user.email,
                "user_uid": str(user.uid),
                "user": user.role,
            },
            refresh=True,
            expire=timedelta(days=1),
        )

        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"uid": str(user.uid), "email": user.email},
            }
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid e-mail or password",
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(
    token_detail: AccessToken = Depends(RefreshTokenBearer()),
):
    expiry_timestamp = token_detail.token["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_detail.token["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")


@auth_router.get("/logout")
async def revoke_token(token_detail: AccessToken = Depends(AccessTokenBearer())):
    jti = token_detail.token["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully"}, status_code=status.HTTP_200_OK
    )
