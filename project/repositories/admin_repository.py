from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from models.administrator import Administrator
from schemas.schemas import AdministratorCreate


class AdminRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_administrators(self) -> List[Administrator]:
        stmt = select(Administrator)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_administrator_by_id(self, administrator_id: int) -> Administrator:
        stmt = select(Administrator).where(Administrator.administrator_id == administrator_id)
        return await self.session.scalar(stmt)

    async def create_administrator(self, administrator: AdministratorCreate) -> Administrator:
        async with self.session.begin_nested():
            created_administrator = Administrator(
                name=administrator.name,
                surname=administrator.surname,
                login=administrator.login,
                password=administrator.password,
                role=administrator.role)
            self.session.add(created_administrator)
            await self.session.commit()
            return created_administrator

    async def update_administrator(self, administrator_id: int, update_data: AdministratorCreate):
        administrator = await self.get_administrator_by_id(administrator_id)
        if administrator is not None:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(administrator, key, value)
            await self.session.commit()
            return administrator
        else:
            raise ValueError("Administrator not found.")

    async def delete_administrator(self, administrator_id: int):
        administrator = await self.get_administrator_by_id(administrator_id)
        await self.session.delete(administrator)
        await self.session.commit()
        return administrator
