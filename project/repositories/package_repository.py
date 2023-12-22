from abc import ABC, abstractmethod
from sqlalchemy import select, update
from typing import List
from models.package import Package
from schemas.schemas import PackageCreate
from database.database import async_session_maker as db_async_session_maker


class AbstractPackageRepository(ABC):
    @abstractmethod
    async def get_all_packages(self) -> List[Package]:
        pass

    @abstractmethod
    async def get_package_by_id(self, package_id: int) -> Package:
        pass

    @abstractmethod
    async def get_package_by_number(self, package_number: int) -> Package:
        pass

    @abstractmethod
    async def get_all_package_by_sender(self, sender_id: int) -> List[Package]:
        pass

    @abstractmethod
    async def create_package(self, package: PackageCreate) -> Package:
        pass

    @abstractmethod
    async def update_package(self, package_id: int, update_data: PackageCreate):
        pass

    @abstractmethod
    async def delete_package(self, package_id: int):
        pass


class PackageRepository(AbstractPackageRepository):

    async def get_all_packages(self) -> List[Package]:
        async with db_async_session_maker() as session:
            stmt = select(Package)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_package_by_id(self, package_id: int) -> Package:
        async with db_async_session_maker() as session:
            stmt = select(Package).where(Package.package_id == package_id)
            return await session.scalar(stmt)

    async def get_package_by_number(self, package_number: int) -> Package:
        async with db_async_session_maker() as session:
            stmt = select(Package).where(Package.number == package_number)
            return await session.scalar(stmt)

    async def get_all_package_by_sender(self, sender_id: int) -> List[Package]:
        async with db_async_session_maker() as session:
            stmt = select(Package).where(Package.sender_id == sender_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def create_package(self, package: PackageCreate) -> Package:
        async with db_async_session_maker() as session:
            created_package = Package(
                number=package.number,
                weight=package.weight,
                sender_id=package.sender_id,
                recipient_id=package.recipient_id,
                status=package.status)
            session.add(created_package)
            await session.commit()
            return created_package

    async def update_package(self, package_id: int, update_data: PackageCreate) -> Package:
        async with db_async_session_maker() as session:
            package = await self.get_package_by_id(package_id)
            if package is not None:
                update_stmt = (
                    update(Package)
                    .where(Package.package_id == package_id)
                    .values(update_data.dict(exclude_unset=True))
                    .returning(Package)
                )
                updated_package = await session.execute(update_stmt)
                await session.commit()
                return updated_package.scalar()
            else:
                raise ValueError("Package not found.")

    async def delete_package(self, package_id: int) -> Package:
        async with db_async_session_maker() as session:
            package = await self.get_package_by_id(package_id)
            await session.delete(package)
            await session.commit()
            return package
