from fastapi import APIRouter, Depends
from services.user_service import UserService
from schemas.schemas import DefaultUserCreate, DefaultUser, Administrator, AdministratorCreate
from typing import List
from enums.roles import Roles


def create_user_router(get_service) -> APIRouter:
    router = APIRouter()

    @router.get("/default_user/{default_user_id}", response_model=DefaultUser)
    async def read_default_user_by_id(
            default_user_id: int,
            service: UserService = Depends(get_service)
    ):
        return await service.read_user_by_id(default_user_id, Roles.ROLE_USER)

    @router.get("/default_user_login/{default_user_login}", response_model=DefaultUser)
    async def read_default_user_by_login(
            default_user_login: str,
            service: UserService = Depends(get_service)
    ):
        return await service.read_default_user_by_login(default_user_login)

    @router.get("/default_user", response_model=List[DefaultUser])
    async def read_all_default_users(
            service: UserService = Depends(get_service)
    ):
        return await service.read_all_default_users()

    @router.post("/default_user", response_model=DefaultUser)
    async def create_default_user(default_user: DefaultUserCreate,
                                  service: UserService = Depends(get_service)):
        return await service.create_default_user(default_user)

    @router.put("/default_user/{default_user_id}", response_model=DefaultUser)
    async def update_default_user(default_user_id: int, default_user: DefaultUserCreate,
                                  service: UserService = Depends(get_service)):
        return await service.update_default_user(default_user_id, default_user)

    @router.delete("/{default_user_id}", response_model=DefaultUser)
    async def delete_default_user(
            default_user_id: int,
            service: UserService = Depends(get_service)
    ):
        return await service.delete_default_user(default_user_id)

    @router.get("/administrator/{administrator_id}", response_model=Administrator)
    async def read_administrator_by_id(
            administrator_id: int,
            service: UserService = Depends(get_service)
    ):
        return await service.read_user_by_id(administrator_id, Roles.ROLE_ADMIN)

    @router.get("/administrator/login/{administrator_login}", response_model=Administrator)
    async def read_administrator_by_login(
            administrator_login: str,
            service: UserService = Depends(get_service)
    ):
        return await service.read_administrator_by_login(administrator_login)

    @router.put("/administrator", response_model=Administrator)
    async def update_administrator(administrator_id: int, administrator: AdministratorCreate,
                                   service: UserService = Depends(get_service)):
        return await service.update_administrator(administrator_id, administrator)

    @router.post("/administrator/{default_user_id}", response_model=Administrator)
    async def change_default_user_role(
            default_user_id: int,
            service: UserService = Depends(get_service)
    ):
        return await service.change_default_user_role(default_user_id)

    return router
