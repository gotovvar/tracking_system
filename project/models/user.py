from sqlalchemy import Column, Integer, String
from database.database import Base


class User(Base):
    __tablename__ = 'user'
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    surname = Column(String(128), nullable=False)
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
