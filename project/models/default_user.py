from sqlalchemy import Column, Enum
from models.user import User
from utils.roles import Roles


class DefaultUser(User):
    __tablename__ = 'default_user'

    role = Column(Enum(Roles), default=Roles.ROLE_USER)
