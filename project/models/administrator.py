from sqlalchemy import Column, Integer, String, Enum
from database.database import Base
from enums.roles import Roles


class Administrator(Base):
    __tablename__ = 'administrator'

    administrator_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    surname = Column(String(128), nullable=False)
    login = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(Enum(Roles), default=Roles.ROLE_ADMIN)
