from __future__ import annotations

from repositories.package_repository import AbstractPackageRepository
from schemas.schemas import PackageCreate


class PackageService:
    def __init__(self, package_rep: AbstractPackageRepository):
        self.package_rep: AbstractPackageRepository = package_rep()

    async def read_all_packages(self):
        return await self.package_rep.get_all_packages()

    async def create_package(self, package: PackageCreate):
        return await self.package_rep.create_package(package)

    async def delete_package(self, package_id: int):
        return await self.package_rep.delete_package(package_id)

    async def read_package_by_number(self, package_number: int):
        return await self.package_rep.get_package_by_number(package_number)

    async def read_all_package_by_sender(self, sender_id: int):
        return await self.package_rep.get_all_package_by_sender(sender_id)

    async def update_package(self, package_id: int, package: PackageCreate):
        return await self.package_rep.update_package(package_id, package)
