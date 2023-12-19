from sqlalchemy import Column, Enum
from models.user import User
from enums.roles import Roles


class Administrator(User):
    __tablename__ = 'administrator'

    role = Column(Enum(Roles), default=Roles.ROLE_ADMIN)
