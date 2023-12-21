from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Union, List
from models.default_user import DefaultUser
from models.administrator import Administrator
from schemas.schemas import DefaultUserCreate, AdministratorCreate
from utils.roles import Roles
from utils.auth import get_hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int, user_role: Roles) -> Union[DefaultUser, Administrator]:
        if user_role == Roles.ROLE_USER:
            stmt = select(DefaultUser).where(DefaultUser.id == user_id)
            return await self.session.scalar(stmt)
        elif user_role == Roles.ROLE_ADMIN:
            stmt = select(Administrator).where(Administrator.id == user_id)
            return await self.session.scalar(stmt)

    async def create_default_user(self, default_user: DefaultUserCreate) -> DefaultUser:
        async with self.session.begin_nested():
            created_default_user = DefaultUser(
                name=default_user.name,
                surname=default_user.surname,
                login=default_user.login,
                password=default_user.password,
                role=default_user.role)
            self.session.add(created_default_user)
            await self.session.commit()
            return created_default_user

    async def create_administrator(self, administrator: Administrator) -> Administrator:
        async with self.session.begin_nested():
            self.session.add(administrator)
            await self.session.flush()
        return administrator

    async def update_default_user(self, default_user_id: int, update_data: DefaultUserCreate) -> DefaultUser:
        default_user = await self.get_user_by_id(default_user_id, Roles.ROLE_USER)
        if default_user:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                if key == "password":
                    value = get_hash_password(value)
                setattr(default_user, key, value)
            await self.session.commit()
            return default_user
        else:
            raise ValueError("User not found.")

    async def update_administrator(self, administrator_id: int, update_data: AdministratorCreate) -> Administrator:
        administrator = await self.get_user_by_id(administrator_id, Roles.ROLE_ADMIN)
        if administrator:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(administrator, key, value)
            await self.session.commit()
            return administrator
        else:
            raise ValueError("User not found.")

    async def get_all_default_users(self) -> List[DefaultUser]:
        stmt = select(DefaultUser)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_default_user(self, default_user_id: int) -> DefaultUser:
        async with self.session.begin_nested():
            default_user = await self.get_user_by_id(default_user_id, Roles.ROLE_USER)
            await self.session.delete(default_user)
            await self.session.commit()
        return default_user

    async def delete_administrator(self, administrator_id: int) -> Administrator:
        administrator = await self.get_user_by_id(administrator_id, Roles.ROLE_ADMIN)
        await self.session.delete(administrator)
        await self.session.commit()
        return administrator

    async def get_default_user_by_login(self, default_user_login: str) -> DefaultUser:
        stmt = select(DefaultUser).where(DefaultUser.login == default_user_login)
        return await self.session.scalar(stmt)

    async def get_administrator_by_login(self, administrator_login: str) -> Administrator:
        stmt = select(Administrator).where(Administrator.login == administrator_login)
        return await self.session.scalar(stmt)

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
