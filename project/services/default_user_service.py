from __future__ import annotations
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from repositories.default_user_repository import DefaultUserRepository
from schemas.schemas import DefaultUserCreate


class DefaultUserService:
    def __init__(self, db: AsyncSession):
        self._database = DefaultUserRepository(db)

    @staticmethod
    @asynccontextmanager
    async def from_engine(engine: AsyncEngine):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield DefaultUserService.from_session(session)

    @staticmethod
    def from_session(session: AsyncSession) -> DefaultUserService:
        database = DefaultUserRepository(session)
        return DefaultUserService(database)

    async def read_all_default_users(self):
        return await self._database.get_all_default_users()

    async def create_default_user(self, default_user: DefaultUserCreate):
        return await self._database.create_default_user(default_user)

    async def delete_default_user(self, default_user_id: int):
        return await self._database.delete_default_user(default_user_id)

    async def read_default_user(self, default_user_id: int):
        return await self._database.get_default_user_by_id(default_user_id)

    async def update_default_user(self, default_user_id: int, default_user: DefaultUserCreate):
        return await self._database.update_default_user(default_user_id, default_user)



