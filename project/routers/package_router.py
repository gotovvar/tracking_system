from fastapi import APIRouter, Depends
from typing import List
from services.package_service import PackageService
from schemas.schemas import Package, PackageCreate


def create_package_router(get_service) -> APIRouter:
    router = APIRouter()

    @router.get("/{package_number}", response_model=Package)
    async def read_package(
            package_number: int,
            service: PackageService = Depends(get_service)
    ):
        return await service.read_package_by_number(package_number)

    @router.get("/sent/{sender_id}", response_model=List[Package])
    async def read_all_package_by_sender(
            sender_id: int,
            service: PackageService = Depends(get_service)
    ):
        return await service.read_all_package_by_sender(sender_id)

    @router.get("/", response_model=List[Package])
    async def read_all_packages(
            service: PackageService = Depends(get_service)
    ):
        return await service.read_all_packages()

    @router.post("/", response_model=Package)
    async def create_package(package: PackageCreate,
                             service: PackageService = Depends(get_service)):
        return await service.create_package(package)

    @router.put("/", response_model=Package)
    async def update_package(package_id: int, package: PackageCreate,
                             service: PackageService = Depends(get_service)):
        return await service.update_package(package_id, package)

    @router.delete("/{package_id}", response_model=Package)
    async def delete_package(
            package_id: int,
            service: PackageService = Depends(get_service)
    ):
        return await service.delete_package(package_id)

    return router



