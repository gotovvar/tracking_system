from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from models.default_user import DefaultUser
from schemas.schemas import DefaultUserCreate


class DefaultUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_default_users(self) -> List[DefaultUser]:
        stmt = select(DefaultUser)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_default_user_by_id(self, default_user_id: int) -> DefaultUser:
        stmt = select(DefaultUser).where(DefaultUser.default_user_id == default_user_id)
        return await self.session.scalar(stmt)

    async def get_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        stmt = select(DefaultUser).where(DefaultUser.login == default_user_login)
        return await self.session.scalar(stmt)

    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        async with self.session.begin_nested():
            created_default_user = DefaultUser(
                name=default_user.name,
                surname=default_user.surname,
                login=default_user.login,
                password=default_user.password,
                role=default_user.role)
            self.session.add(created_default_user)
            await self.session.commit()
            return created_default_user

    async def update_default_user(self, default_user_id: int, update_data: DefaultUserCreate):
        default_user = await self.get_default_user_by_id(default_user_id)
        if default_user is not None:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(default_user, key, value)
            await self.session.commit()
            return default_user
        else:
            raise ValueError("User not found.")

    async def delete_default_user(self, default_user_id: int):
        default_user = await self.get_default_user_by_id(default_user_id)
        await self.session.delete(default_user)
        await self.session.commit()
        return default_user
