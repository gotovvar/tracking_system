from __future__ import annotations
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from utils.roles import Roles
from repositories.user_repository import UserRepository
from schemas.schemas import DefaultUserCreate, AdministratorCreate
from models.default_user import DefaultUser
from models.administrator import Administrator
from typing import Union, List


class UserService:
    def __init__(self, db: AsyncSession):
        self._database = UserRepository(db)

    @staticmethod
    @asynccontextmanager
    async def from_engine(engine: AsyncEngine):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield UserService.from_session(session)

    @staticmethod
    def from_session(session: AsyncSession) -> UserService:
        database = UserRepository(session)
        return UserService(database)

    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        return await self._database.create_default_user(default_user)

    async def read_user_by_id(self, default_user_id: int, role: Roles) -> Union[DefaultUser, Administrator]:
        return await self._database.get_user_by_id(default_user_id, role)

    async def read_all_default_users(self) -> List[DefaultUser]:
        return await self._database.get_all_default_users()

    async def update_administrator(self, administrator_id: int, administrator: AdministratorCreate) -> Administrator:
        return await self._database.update_administrator(administrator_id, administrator)

    async def update_default_user(self, default_user_id: int, default_user: DefaultUserCreate) -> DefaultUser:
        return await self._database.update_default_user(default_user_id, default_user)

    async def delete_default_user(self, default_user_id: int) -> DefaultUser:
        return await self._database.delete_default_user(default_user_id)

    async def delete_administrator(self, administrator_id: int) -> Administrator:
        return await self._database.delete_administrator(administrator_id)

    async def read_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        return await self._database.get_default_user_by_login(default_user_login)

    async def read_administrator_by_login(self, administrator_login: str) -> Administrator:
        return await self._database.get_administrator_by_login(administrator_login)

    async def change_default_user_role(self, default_user_id: int) -> Administrator:
        return await self._database.change_default_user_role(default_user_id)
