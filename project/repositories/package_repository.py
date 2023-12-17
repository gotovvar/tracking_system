from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from models.package import Package
from schemas.schemas import PackageCreate


class PackageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_packages(self) -> List[Package]:
        stmt = select(Package)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_package_by_id(self, package_id: int) -> Package:
        stmt = select(Package).where(Package.package_id == package_id)
        return await self.session.scalar(stmt)

    async def create_package(self, package: PackageCreate) -> Package:
        async with self.session.begin_nested():
            created_package = Package(
                number=package.number,
                weight=package.weight,
                sender_id=package.sender_id,
                recipient_id=package.recipient_id,
                status=package.role)
            self.session.add(created_package)
            await self.session.commit()
            return created_package

    async def update_package(self, package_id: int, update_data: PackageCreate):
        package = await self.get_package_by_id(package_id)
        if package is not None:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(package, key, value)
            await self.session.commit()
            return package
        else:
            raise ValueError("User not found.")

    async def delete_package(self, package_id: int):
        package = await self.get_package_by_id(package_id)
        await self.session.delete(package)
        await self.session.commit()
        return package
