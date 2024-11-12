from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel
from .models import User
from .utils import encrypt_password


class UserService:
    async def get_user(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user(email, session)

        if user is None:
            return False

        return True

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = encrypt_password(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user
