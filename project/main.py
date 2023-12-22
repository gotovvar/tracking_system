from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.user_service import UserService
from services.package_service import PackageService
from repositories.package_repository import PackageRepository
from repositories.user_repository import UserRepository
from routers.user_router import UserRouter
from routers.package_router import PackageRouter
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


user_service = UserService(UserRepository)

user_router = UserRouter(user_service)
app.include_router(user_router, prefix="/user", tags=["user"])

package_service = PackageService(PackageRepository)

package_route = PackageRouter(package_service)
app.include_router(package_route, prefix="/package", tags=["package"])

auth_route = create_auth_router(user_service)
app.include_router(auth_route, prefix="/auth", tags=["auth"])

pages_route = create_pages_router()
app.include_router(pages_route, prefix="/pages", tags=["pages"])
