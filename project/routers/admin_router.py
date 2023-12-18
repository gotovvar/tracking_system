from fastapi import APIRouter, Depends
from typing import List
from services.administrator_service import AdminService
from schemas.schemas import Administrator, AdministratorCreate


def create_admin_router(
        get_service
) -> APIRouter:
    router = APIRouter()

    @router.get("/{administrator_id}", response_model=Administrator)
    async def read_administrator(
            administrator_id: int,
            service: AdminService = Depends(get_service)
    ):
        return await service.read_administrator(administrator_id)

    @router.get("/", response_model=List[Administrator])
    async def read_all_administrators(
            service: AdminService = Depends(get_service)
    ):
        return await service.read_all_administrators()

    @router.post("/", response_model=Administrator)
    async def create_administrator(administrator: AdministratorCreate,
                                   service: AdminService = Depends(get_service)):
        return await service.create_administrator(administrator)

    @router.put("/", response_model=Administrator)
    async def update_package(administrator_id: int, administrator: AdministratorCreate,
                             service: AdminService = Depends(get_service)):
        return await service.update_administrator(administrator_id, administrator)

    @router.delete("/{administrator_id}", response_model=Administrator)
    async def delete_package(
            administrator_id: int,
            service: AdminService = Depends(get_service)
    ):
        return await service.delete_administrator(administrator_id)

    return router



