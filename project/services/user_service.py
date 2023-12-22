from __future__ import annotations
from sqlalchemy.ext.asyncio.session import AsyncSession
from utils.roles import Roles
from repositories.user_repository import AbstractUserRepository
from schemas.schemas import DefaultUserCreate, AdministratorCreate
from models.default_user import DefaultUser
from models.administrator import Administrator
from typing import Union, List


class UserService:
    def __init__(self, user_rep: AbstractUserRepository):
        self.user_rep: AbstractUserRepository = user_rep()

    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        return await self.user_rep.create_default_user(default_user)

    async def read_user_by_id(self, default_user_id: int, role: Roles) -> Union[DefaultUser, Administrator]:
        return await self.user_rep.get_user_by_id(default_user_id, role)

    async def read_all_default_users(self) -> List[DefaultUser]:
        return await self.user_rep.get_all_default_users()

    async def update_administrator(self, administrator_id: int, administrator: AdministratorCreate) -> Administrator:
        return await self.user_rep.update_administrator(administrator_id, administrator)

    async def update_default_user(self, default_user_id: int, default_user: DefaultUserCreate) -> DefaultUser:
        return await self.user_rep.update_default_user(default_user_id, default_user)

    async def delete_default_user(self, default_user_id: int) -> DefaultUser:
        return await self.user_rep.delete_default_user(default_user_id)

    async def delete_administrator(self, administrator_id: int) -> Administrator:
        return await self.user_rep.delete_administrator(administrator_id)

    async def read_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        return await self.user_rep.get_default_user_by_login(default_user_login)

    async def read_administrator_by_login(self, administrator_login: str) -> Administrator:
        return await self.user_rep.get_administrator_by_login(administrator_login)

    async def change_default_user_role(self, default_user_id: int) -> Administrator:
        return await self.user_rep.change_default_user_role(default_user_id)
