from fastapi import APIRouter
from typing import List
from services.package_service import PackageService
from schemas.schemas import Package, PackageCreate


class PackageRouter(APIRouter):
    def __init__(self, package_service: PackageService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.package_service = package_service
        self.setup_routes()

    def setup_routes(self):
        self.add_api_route("/{package_number}", self.read_package, methods=["GET"], response_model=Package)
        self.add_api_route("/", self.read_all_packages, methods=["GET"], response_model=List[Package])
        self.add_api_route("/sent/{sender_id}", self.read_all_package_by_sender, methods=["GET"], response_model=List[Package])
        self.add_api_route("/", self.create_package, methods=["POST"], response_model=Package)
        self.add_api_route("/", self.update_package, methods=["PUT"], response_model=Package)
        self.add_api_route("/{package_id}", self.delete_package, methods=["DELETE"], response_model=Package)

    async def read_package(self, package_number: int):
        return await self.package_service.read_package_by_number(package_number)

    async def read_all_package_by_sender(self, sender_id: int):
        return await self.package_service.read_all_package_by_sender(sender_id)

    async def read_all_packages(self):
        return await self.package_service.read_all_packages()

    async def create_package(self, package: PackageCreate):
        return await self.package_service.create_package(package)

    async def update_package(self, package_id: int, package: PackageCreate):
        return await self.package_service.update_package(package_id, package)

    async def delete_package(self, package_id: int):
        return await self.package_service.delete_package(package_id)




