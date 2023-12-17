from fastapi import FastAPI, Depends
from repositories.default_user_repository import DefaultUserRepository
from database.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from database.database import async_engine
from services.default_user_service import DefaultUserService
from services.administrator_service import AdminService
import schemas.schemas as schemas
from typing import List


app = FastAPI()

SessionLocal = async_sessionmaker(expire_on_commit=False, bind=async_engine)


async def get_user_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = DefaultUserService(session)
            yield service


async def get_administrator_service():
    async with SessionLocal() as session:
        async with session.begin():
            service = AdminService(session)
            yield service


@app.get("/user/{user_id}", response_model=schemas.DefaultUser)
async def read_default_user(
        user_id: int,
        service: DefaultUserService = Depends(get_user_service)
):
    return await service.read_default_user(user_id)


@app.get("/user", response_model=List[schemas.DefaultUser])
async def read_default_user(
        service: DefaultUserService = Depends(get_user_service)
):
    return await service.read_all_default_users()


@app.post("/user", response_model=schemas.DefaultUser)
async def create_user(user: schemas.DefaultUserCreate, service: DefaultUserService = Depends(get_user_service)):
    return await service.create_default_user(user)


@app.put("/user", response_model=schemas.DefaultUser)
async def create_user(user_id: int, user: schemas.DefaultUserCreate, service: DefaultUserService = Depends(get_user_service)):
    return await service.update_default_user(user_id, user)


@app.delete("/user/{user_id}", response_model=schemas.DefaultUser)
async def delete_user(
        user_id: int,
        service: DefaultUserService = Depends(get_user_service)
):
    return await service.delete_default_user(user_id)


@app.get("/administrator/{administrator_id}", response_model=schemas.Administrator)
async def read_administrator(
        administrator_id: int,
        service: AdminService = Depends(get_administrator_service)
):
    return await service.read_administrator(administrator_id)


@app.get("/administrator", response_model=List[schemas.Administrator])
async def read_administrator(
        service: AdminService = Depends(get_administrator_service)
):
    return await service.read_all_administrators()


@app.post("/administrator", response_model=schemas.Administrator)
async def create_administrator(administrator: schemas.AdministratorCreate, service: AdminService = Depends(get_administrator_service)):
    return await service.create_administrator(administrator)


@app.put("/administrator", response_model=schemas.Administrator)
async def create_administrator(administrator_id: int, administrator: schemas.AdministratorCreate, service: AdminService = Depends(get_administrator_service)):
    return await service.update_administrator(administrator_id, administrator)


@app.delete("/administrator/{administrator_id}", response_model=schemas.Administrator)
async def delete_user(
        administrator_id: int,
        service: AdminService = Depends(get_administrator_service)
):
    return await service.delete_administrator(administrator_id)
