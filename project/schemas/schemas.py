from pydantic import BaseModel
from enums.status import Status
from enums.roles import Roles


class Package(BaseModel):
    package_id: int
    number: int
    weight: float
    sender_id: int
    recipient_id: int
    status: Status

    class Config:
        from_attributes = True


class PackageCreate(BaseModel):
    number: int
    weight: float
    sender_id: int
    recipient_id: int
    status: Status = Status.IN_WAREHOUSE


class DefaultUser(BaseModel):
    default_user_id: int
    name: str
    surname: str
    login: str
    password: str
    role: Roles = Roles.ROLE_USER


class DefaultUserCreate(BaseModel):
    name: str
    surname: str
    login: str
    password: str
    role: Roles = Roles.ROLE_USER


class Administrator(BaseModel):
    administrator_id: int
    name: str
    surname: str
    login: str
    password: str
    role: Roles = Roles.ROLE_ADMIN


class AdministratorCreate(BaseModel):
    name: str
    surname: str
    login: str
    password: str
    role: Roles = Roles.ROLE_ADMIN
