from typing import Optional, List
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from src.db.models import User
from .schemas import AccessToken
from .utils import decode_token
from .service import UserService

user_service = UserService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[AccessToken] | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self.is_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "Error": "This token is invalid or expired",
                    "resolution": "Please get new token",
                },
            )

        token_data = decode_token(token)

        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "Error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token",
                },
            )

        self.verify_token_data(token_data)

        access_token = AccessToken(token=token_data)

        return access_token

    def is_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True

        return False

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token",
            )


async def get_current_user(
    token_details: AccessToken = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details.token["user"]["email"]
    user = await user_service.get_user(user_email, session)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action",
        )
