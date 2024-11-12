from typing import Optional
from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy import values

from .schemas import AccessToken
from .utils import decode_token


class AcessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[AccessToken] | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self.is_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )

        token_data = decode_token(token)

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )

        access_token = AccessToken(token=token_data)

        return access_token

    def is_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True

        return False
