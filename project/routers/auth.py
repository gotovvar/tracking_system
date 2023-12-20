from pydantic import BaseModel, ConfigDict, ValidationError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from typing import Union, Annotated
from utils.auth import get_hash_password, verify_password, create_access_token
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from config import SECRET_AUTH, AUTH_ALGORITHM
from utils.roles import Roles
from services.user_service import UserService
from schemas.schemas import DefaultUserCreate, DefaultUser, Administrator

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None

    model_config = ConfigDict(from_attributes=True)


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
        hashed_password = get_hash_password(password)
        default_user = DefaultUserCreate(
            name=name,
            surname=surname,
            login=login,
            password=hashed_password,
            role=Roles.ROLE_USER
        )
        return await service.create_default_user(default_user)

    @router.post("/login")
    async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(get_user_service)
    ):
        user = await _authenticate_user(form_data.username, form_data.password, user_service)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"access_token": create_access_token(user.login), "token_type": "bearer"}

    async def read_current_user(
            token: str = Depends(oauth2_scheme),
            user_service: UserService = Depends(get_user_service)
    ) -> Union[DefaultUser, Administrator, None]:
        try:
            payload = jwt.decode(token, SECRET_AUTH, algorithms=[AUTH_ALGORITHM])
            token_data = TokenPayload(**payload)
        except (jwt.exceptions.DecodeError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.exceptions.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            user = await _get_user(token_data.sub, user_service)
        except Exception as e:
            raise e
        return user

    @router.get("/current_user")
    async def get_current_user(current_user: Union[DefaultUser, Administrator] = Depends(read_current_user)):
        return current_user

    @router.post("/logout")
    async def logout_user():
        response = ORJSONResponse({"message": "User has been logged out"})
        response.delete_cookie(key="access_token")

        return response

    async def _get_user(login: str,
                        user_service: UserService = Depends(get_user_service)
                        ) -> Union[Administrator, DefaultUser, None]:
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
        return None

    async def _authenticate_user(login: str, password: str,
                                 user_service: UserService = Depends(get_user_service)
                                 ) -> Union[Administrator, DefaultUser, None]:
        user = await _get_user(login, user_service)
        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    return router



