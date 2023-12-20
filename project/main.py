from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.database import async_engine
from services.user_service import UserService
from services.package_service import PackageService
from routers.user_router import create_user_router
from routers.package_router import create_package_router
from routers.auth import create_auth_router
from routers.pages import create_pages_router

app = FastAPI(
    title='tracking-system'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH"],
    allow_headers=["*"],
)

SessionLocal = async_sessionmaker(expire_on_commit=False, bind=async_engine)


async def get_package_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = PackageService(session)
            yield service


async def get_user_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = UserService(session)
            yield service

user_router = create_user_router(get_user_service)
app.include_router(user_router, prefix="/user", tags=["user"])

package_route = create_package_router(get_package_service)
app.include_router(package_route, prefix="/package", tags=["package"])

auth_route = create_auth_router(get_user_service)
app.include_router(auth_route, prefix="/auth", tags=["auth"])

pages_route = create_pages_router(get_user_service)
app.include_router(pages_route, prefix="/pages", tags=["pages"])

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