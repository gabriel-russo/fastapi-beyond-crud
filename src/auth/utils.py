from passlib.context import CryptContext
import jwt
from uuid import uuid4
from datetime import datetime, timedelta
from src.config import config

passwd_context = CryptContext(schemes=["bcrypt"])


def encrypt_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(
    user_data: dict, expire: timedelta = timedelta(seconds=3600), refresh: bool = False
):
    payload = {}

    payload.update(
        user=user_data,
        exp=(datetime.now() + expire).timestamp(),
        jti=str(uuid4()),
        refresh=refresh,
    )

    token = jwt.encode(
        payload=payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )

    except jwt.PyJWTError as err:
        print(err)
        return None
