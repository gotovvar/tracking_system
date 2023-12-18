from __future__ import annotations
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from repositories.admin_repository import AdminRepository
from schemas.schemas import AdministratorCreate


class AdminService:
    def __init__(self, db: AsyncSession):
        self._database = AdminRepository(db)

    @staticmethod
    @asynccontextmanager
    async def from_engine(engine: AsyncEngine):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield AdminService.from_session(session)

    @staticmethod
    def from_session(session: AsyncSession) -> AdminService:
        database = AdminRepository(session)
        return AdminService(database)

    async def read_all_administrators(self):
        return await self._database.get_all_administrators()

    async def create_administrator(self, administrator: AdministratorCreate):
        return await self._database.create_administrator(administrator)

    async def delete_administrator(self, administrator_id: int):
        return await self._database.delete_administrator(administrator_id)

    async def read_administrator_by_id(self, administrator_id: int):
        return await self._database.get_administrator_by_id(administrator_id)

    async def read_administrator_by_login(self, administrator_login: str):
        return await self._database.get_administrator_by_login(administrator_login)

    async def update_administrator(self, administrator_id: int, administrator: AdministratorCreate):
        return await self._database.update_administrator(administrator_id, administrator)



