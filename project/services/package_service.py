from __future__ import annotations
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from repositories.package_repository import PackageRepository
from schemas.schemas import PackageCreate


class PackageService:
    def __init__(self, db: AsyncSession):
        self._database = PackageRepository(db)

    @staticmethod
    @asynccontextmanager
    async def from_engine(engine: AsyncEngine):
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield PackageService.from_session(session)

    @staticmethod
    def from_session(session: AsyncSession) -> PackageService:
        database = PackageRepository(session)
        return PackageService(database)

    async def read_all_packages(self):
        return await self._database.get_all_packages()

    async def create_package(self, package: PackageCreate):
        return await self._database.create_package(package)

    async def delete_package(self, package_id: int):
        return await self._database.delete_package(package_id)

    async def read_package_by_number(self, package_number: int):
        return await self._database.get_package_by_number(package_number)

    async def read_all_package_by_sender(self, sender_id: int):
        return await self._database.get_all_package_by_sender(sender_id)

    async def update_package(self, package_id: int, package: PackageCreate):
        return await self._database.update_package(package_id, package)
