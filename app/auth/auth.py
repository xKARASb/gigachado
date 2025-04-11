from os import getenv

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError

from secrets import token_hex

from ..db import get_db
from .utils import verify_password, get_password_hash
from .models import User

from ..db.repos import EmployeeRepository
from ..db.schemas.employee import EmployeeInput


load_dotenv("./app/cfg/auth.env")

oauth2scheme = OAuth2PasswordBearer("/auth/token")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")


async def authenticate_user(first_name: str, last_name: str, patronymic:str, password: str, session):
    users = EmployeeRepository(session).get_by_fullname(first_name, last_name, patronymic)
    if len(users) == 0:
        return False
    for user in users:
        if verify_password(password, user.password):
            return user
    return False        

async def refresh_token_user(id: str, token: str, session):
    user = EmployeeRepository(session).get_by_id(id)
    if user is None:
        return False
    if token == user.refresh_token:
        return user
    return False        


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(user: User, session):
    token = token_hex(16)
    user = EmployeeRepository(session).update_refresh_token(user.id, token)
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id: str = payload.get("id")
        print(id)
        if id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = EmployeeRepository(next(get_db())).get_user(id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

async def user_password_hash(user: EmployeeInput) -> EmployeeInput:
    user.password = get_password_hash(user.password)
    return user