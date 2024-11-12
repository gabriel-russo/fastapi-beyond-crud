from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from .schemas import UserCreateModel
from .service import UserService
from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session

auth_router = APIRouter()

user_service = UserService()


@auth_router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
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
