from datetime import timedelta
# from typing import Annotated

from os import getenv
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import load_dotenv
from .auth import authenticate_user, create_access_token, refresh_token_user, create_refresh_token, get_current_active_user
from .schemas import TokenResponse, RefreshTokenRequestForm, AccessTokenRequestForm

from sqlalchemy.orm import Session
from ..db import get_db
# from db.repos import EmployeeRepository
# from db.schemas.employee import EmployeeInput
# from ..repository.db import get_db, UserRepository
# from ..repository.db.schemas.auth import UserInput

load_dotenv("./app/cfg/auth.env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# @auth_router.post("/registration", response_model=UserRegistrationResponse)
# async def new_user(
#     data: UserRegistrationForm,
#     session: Session = Depends(get_db)
# ):
#     new_user = UserInput(
#         email=data.email,
#         fullname=data.fullname,
#         password=data.password
#     )
#     if UserRepository(session).user_exists_by_email(new_user.email):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with this email already exsist",
#         )
#     user = UserRepository(session).create(await user_password_hash(new_user))
#     return UserRegistrationResponse(
#         id=user.id,
#         email=user.email,
#         fullname=user.fullname
#     )

@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: AccessTokenRequestForm,
    session: Session = Depends(get_db)
) -> TokenResponse:
    user = await authenticate_user(form_data.first, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id, "password": user.password}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(user, session)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    form_data: RefreshTokenRequestForm,
    session: Session = Depends(get_db)
) -> TokenResponse:
    user = await refresh_token_user(form_data.email, form_data.refresh_token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or refresh_token",
            headers={"Authorization": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user.id, "password": user.password}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(user, session)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")