from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from typing import Union

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from config import SECRET_AUTH, AUTH_ALGORITHM, AUTH_ACCESS_TOKEN_EXPIRE_MINUTES
from enums.roles import Roles
from services.user_service import UserService
from schemas.schemas import DefaultUserCreate, DefaultUser, Administrator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_auth_router(get_user_service) -> APIRouter:
    router = APIRouter()

    @router.post("/register/{name}/{surname}/{login}/{password}")
    async def register_default_user(
            name: str,
            surname: str,
            login: str,
            password: str,
            service: UserService = Depends(get_user_service),
    ):
        hashed_password = hash_password(password)
        default_user = DefaultUserCreate(
            name=name,
            surname=surname,
            login=login,
            password=hashed_password,
            role=Roles.ROLE_USER
        )
        return await service.create_default_user(default_user)

    @router.post("/login/{login}/{password}")
    async def login_user(
        login: str,
        password: str,
        user_service: UserService = Depends(get_user_service)
    ):
        user = await _authenticate_user(login, password, user_service)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=int(AUTH_ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        response = ORJSONResponse(
            {"access_token": access_token, "token_type": "bearer"}
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            expires=access_token_expires.total_seconds(),
            httponly=True,
        )
        return response

    async def get_current_user(
            token: str = Depends(oauth2_scheme),
            user_service: UserService = Depends(get_user_service)
    ) -> Union[DefaultUser, Administrator]:
        try:
            payload = jwt.decode(token, SECRET_AUTH, algorithms=[AUTH_ALGORITHM])
            login: str = payload.get("sub")
            if login is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user = await _get_user(login, user_service)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user
        except PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def _get_user(login: str,
                        user_service: UserService = Depends(get_user_service)
                        ) -> Union[Administrator, DefaultUser, False]:
        try:
            result = await user_service.read_default_user_by_login(default_user_login=login)
            if result:
                return result
        except:
            pass
        try:
            result = await user_service.read_administrator_by_login(administrator_login=login)
            if result:
                return result
        except:
            pass
        return False

    def __verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def _authenticate_user(login: str, password: str,
                                 user_service: UserService = Depends(get_user_service)
                                 ) -> Union[Administrator, DefaultUser, False]:
        user = await _get_user(login, user_service)
        if not user:
            return False

        if not __verify_password(password, user.password):
            return False

        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_AUTH, algorithm=AUTH_ALGORITHM)
        return encoded_jwt

    @router.get("/current_user")
    async def get_current_user(current_user: Union[DefaultUser, Administrator] = Depends(get_current_user)):
        return current_user

    @router.post("/logout")
    async def logout_user():
        response = ORJSONResponse({"message": "User has been logged out"})
        response.delete_cookie(key="access_token")

        return response

    return router


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
