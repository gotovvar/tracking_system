from fastapi import FastAPI, Depends
from repositories.default_user_repository import DefaultUserRepository
from database.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from database.database import async_engine
from services.default_user_service import DefaultUserService
from services.administrator_service import AdminService
from services.package_service import PackageService
from routers.default_user_router import create_default_user_router
from routers.package_router import create_package_router
from routers.admin_router import create_admin_router

app = FastAPI(
    title='tracking-system'
)

SessionLocal = async_sessionmaker(expire_on_commit=False, bind=async_engine)


async def get_administrator_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = AdminService(session)
            yield service


async def get_package_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = PackageService(session)
            yield service


async def get_user_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = DefaultUserService(session)
            yield service

user_router = create_default_user_router(get_user_service)
app.include_router(user_router, prefix="/default_user", tags=["default_user"])

package_route = create_package_router(get_package_service)
app.include_router(package_route, prefix="/package", tags=["package"])

admin_route = create_admin_router(get_administrator_service)
app.include_router(admin_route, prefix="/administrator", tags=["administrator"])


"""
class DefaultUserRouter(APIRouter):
    def __init__(self, service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
        self.setup_routes()

    def setup_routes(self):
        self.add_api_route("/{user_id}", self.read_default_user, methods=["GET"])
        self.add_api_route("/", self.read_all_default_users, methods=["GET"])
        self.add_api_route("/", self.create_default_user, methods=["POST"])
        self.add_api_route("/{user_id}", self.update_default_user, methods=["PUT"])
        self.add_api_route("/{user_id}", self.delete_default_user, methods=["DELETE"])

    async def read_default_user(self, default_user_id: int):
        return await self.service.read_default_user(default_user_id)

    async def read_all_default_users(self):
        return await self.service.read_all_default_users()

    async def create_default_user(self, default_user: DefaultUserCreate):
        return await self.service.create_default_user(default_user)

    async def update_default_user(self, default_user_id: int, default_user: DefaultUserCreate):
        return await self.service.update_default_user(default_user_id, default_user)

    async def delete_default_user(self, default_user_id: int):
        return await self.service.delete_default_user(default_user_id)
"""