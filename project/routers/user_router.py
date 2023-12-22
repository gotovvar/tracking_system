from fastapi import APIRouter, Depends
from typing import List
from services.user_service import UserService
from schemas.schemas import DefaultUser, DefaultUserCreate, Administrator, AdministratorCreate
from utils.roles import Roles


class UserRouter(APIRouter):
    def __init__(self, user_service: UserService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        self.add_api_route("/default_user/{default_user_id}", self.read_default_user_by_id, methods=["GET"], response_model=DefaultUser)
        self.add_api_route("/default_user_login/{default_user_login}", self.read_default_user_by_login, methods=["GET"], response_model=DefaultUser)
        self.add_api_route("/default_user", self.read_all_default_users, methods=["GET"], response_model=List[DefaultUser])
        self.add_api_route("/default_user", self.create_default_user, methods=["POST"], response_model=DefaultUser)
        self.add_api_route("/default_user/{default_user_id}", self.update_default_user, methods=["PUT"], response_model=DefaultUser)
        self.add_api_route("/{default_user_id}", self.delete_default_user, methods=["DELETE"], response_model=DefaultUser)

        self.add_api_route("/admin/{admin_id}", self.delete_admin, methods=["DELETE"], response_model=Administrator)
        self.add_api_route("/administrator/{administrator_id}", self.read_administrator_by_id, methods=["GET"], response_model=Administrator)
        self.add_api_route("/administrator/login/{administrator_login}", self.read_administrator_by_login, methods=["GET"], response_model=Administrator)
        self.add_api_route("/administrator", self.update_administrator, methods=["PUT"], response_model=Administrator)
        self.add_api_route("/administrator/{default_user_id}", self.change_default_user_role, methods=["POST"], response_model=Administrator)

    async def read_default_user_by_id(self, default_user_id: int):
        return await self.user_service.read_user_by_id(default_user_id, Roles.ROLE_USER)

    async def read_default_user_by_login(self, default_user_login: str):
        return await self.user_service.read_default_user_by_login(default_user_login)

    async def read_all_default_users(self):
        return await self.user_service.read_all_default_users()

    async def create_default_user(self, default_user: DefaultUserCreate):
        return await self.user_service.create_default_user(default_user)

    async def update_default_user(self, default_user_id: int, default_user: DefaultUserCreate):
        return await self.user_service.update_default_user(default_user_id, default_user)

    async def delete_default_user(self, default_user_id: int):
        return await self.user_service.delete_default_user(default_user_id)

    async def delete_admin(self, admin_id: int):
        return await self.user_service.delete_administrator(admin_id)

    async def read_administrator_by_id(self, administrator_id: int):
        return await self.user_service.read_user_by_id(administrator_id, Roles.ROLE_ADMIN)

    async def read_administrator_by_login(self, administrator_login: str):
        return await self.user_service.read_administrator_by_login(administrator_login)

    async def update_administrator(self, administrator_id: int, administrator: AdministratorCreate):
        return await self.user_service.update_administrator(administrator_id, administrator)

    async def change_default_user_role(self, default_user_id: int):
        return await self.user_service.change_default_user_role(default_user_id)
