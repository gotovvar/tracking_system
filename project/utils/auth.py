from datetime import datetime, timedelta
from typing import Any, Union

import jwt
from passlib.context import CryptContext

from config import AUTH_ALGORITHM, AUTH_ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_AUTH

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(key: str, subject: Union[str, Any], expires_delta):
    expire = datetime.utcnow() + timedelta(minutes=int(expires_delta))
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, key, AUTH_ALGORITHM)
    return encoded_jwt


def create_access_token(
    subject: Union[str, Any],
    expires_delta: int = AUTH_ACCESS_TOKEN_EXPIRE_MINUTES,
) -> str:
    return create_token(SECRET_AUTH, subject, expires_delta)
