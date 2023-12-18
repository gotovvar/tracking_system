from fastapi import APIRouter, Depends
from services.default_user_service import DefaultUserService
from schemas.schemas import DefaultUserCreate, DefaultUser
from typing import List


def create_default_user_router(
        get_service
) -> APIRouter:
    router = APIRouter()

    @router.get("/{default_user_id}", response_model=DefaultUser)
    async def read_default_user(
            default_user_id: int,
            service: DefaultUserService = Depends(get_service)
    ):
        return await service.read_default_user(default_user_id)

    @router.get("/", response_model=List[DefaultUser])
    async def read_all_default_users(
            service: DefaultUserService = Depends(get_service)
    ):
        return await service.read_all_default_users()

    @router.post("/", response_model=DefaultUser)
    async def create_default_user(default_user: DefaultUserCreate,
                                  service: DefaultUserService = Depends(get_service)):
        return await service.create_default_user(default_user)

    @router.put("/", response_model=DefaultUser)
    async def update_default_user(default_user_id: int, default_user: DefaultUserCreate,
                                  service: DefaultUserService = Depends(get_service)):
        return await service.update_default_user(default_user_id, default_user)

    @router.delete("/{default_user_id}", response_model=DefaultUser)
    async def delete_default_user(
            default_user_id: int,
            service: DefaultUserService = Depends(get_service)
    ):
        return await service.delete_default_user(default_user_id)

    return router
