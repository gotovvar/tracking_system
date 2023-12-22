from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Union, List
from models.default_user import DefaultUser
from models.administrator import Administrator
from schemas.schemas import DefaultUserCreate, AdministratorCreate
from utils.roles import Roles
from utils.auth import get_hash_password
from database.database import async_session_maker as db_async_session_maker


class AbstractUserRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_user_by_id(self, user_id: int, user_role: Roles) -> Union[DefaultUser, Administrator]:
        pass

    @abstractmethod
    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        pass

    @abstractmethod
    async def create_administrator(self, administrator: AdministratorCreate) -> Administrator:
        pass

    @abstractmethod
    async def update_default_user(self, default_user_id: int, update_data: DefaultUserCreate) -> DefaultUser:
        pass

    @abstractmethod
    async def update_administrator(self, administrator_id: int, update_data: AdministratorCreate) -> Administrator:
        pass

    @abstractmethod
    async def get_all_default_users(self) -> List[DefaultUser]:
        pass

    @abstractmethod
    async def delete_default_user(self, default_user_id: int) -> DefaultUser:
        pass

    @abstractmethod
    async def delete_administrator(self, administrator_id: int) -> Administrator:
        pass

    @abstractmethod
    async def get_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        pass

    @abstractmethod
    async def get_administrator_by_login(self, administrator_login: str) -> Administrator:
        pass

    @abstractmethod
    async def change_default_user_role(self, default_user_id: int) -> Administrator:
        pass


class UserRepository:

    async def get_user_by_id(self, user_id: int, user_role: Roles) -> Union[DefaultUser, Administrator]:
        async with db_async_session_maker() as session:
            if user_role == Roles.ROLE_USER:
                stmt = select(DefaultUser).where(DefaultUser.id == user_id)
                return await session.scalar(stmt)
            elif user_role == Roles.ROLE_ADMIN:
                stmt = select(Administrator).where(Administrator.id == user_id)
                return await session.scalar(stmt)

    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        async with db_async_session_maker() as session:
            async with session.begin_nested():
                created_default_user = DefaultUser(
                    name=default_user.name,
                    surname=default_user.surname,
                    login=default_user.login,
                    password=default_user.password,
                    role=default_user.role)
                session.add(created_default_user)
                await session.commit()
                return created_default_user

    async def create_administrator(self, administrator: Administrator) -> Administrator:
        async with db_async_session_maker() as session:
            session.add(administrator)
            await session.commit()
            return administrator

    async def update_default_user(self, default_user_id: int, update_data: DefaultUserCreate) -> DefaultUser:
        async with db_async_session_maker() as session:
            default_user = await self.get_user_by_id(default_user_id, Roles.ROLE_USER)
            if default_user:
                if get_hash_password(update_data.password) != default_user.password:
                    update_data.password = get_hash_password(update_data.password)

                update_stmt = (
                    update(DefaultUser)
                    .where(DefaultUser.id == default_user_id)
                    .values(update_data.dict(exclude_unset=True))
                    .returning(DefaultUser)
                )
                updated_user = await session.execute(update_stmt)
                await session.commit()
                return updated_user.scalar()
            else:
                raise ValueError("User not found.")

    async def update_administrator(self, administrator_id: int, update_data: AdministratorCreate) -> Administrator:
        async with db_async_session_maker() as session:
            administrator = await self.get_user_by_id(administrator_id, Roles.ROLE_ADMIN)
            if administrator:
                for key, value in update_data.model_dump(exclude_unset=True).items():
                    setattr(administrator, key, value)
                await session.commit()
                return administrator
            else:
                raise ValueError("User not found.")

    async def get_all_default_users(self) -> List[DefaultUser]:
        async with db_async_session_maker() as session:
            stmt = select(DefaultUser)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def delete_default_user(self, default_user_id: int) -> DefaultUser:
        async with db_async_session_maker() as session:
            default_user = await self.get_user_by_id(default_user_id, Roles.ROLE_USER)
            await session.delete(default_user)
            await session.commit()
            return default_user

    async def delete_administrator(self, administrator_id: int) -> Administrator:
        async with db_async_session_maker() as session:
            administrator = await self.get_user_by_id(administrator_id, Roles.ROLE_ADMIN)
            await session.delete(administrator)
            await session.commit()
            return administrator

    async def get_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        async with db_async_session_maker() as session:
            stmt = select(DefaultUser).where(DefaultUser.login == default_user_login)
            return await session.scalar(stmt)

    async def get_administrator_by_login(self, administrator_login: str) -> Administrator:
        async with db_async_session_maker() as session:
            stmt = select(Administrator).where(Administrator.login == administrator_login)
            return await session.scalar(stmt)

    async def change_default_user_role(self, default_user_id: int) -> Administrator:
        user = await self.get_user_by_id(default_user_id, Roles.ROLE_USER)
        if user:
            administrator = Administrator(
                name=user.name,
                surname=user.surname,
                login=user.login,
                password=user.password)
            await self.create_administrator(administrator)
            await self.delete_default_user(user.id)
            return user
