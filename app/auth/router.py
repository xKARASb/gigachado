from datetime import timedelta
from typing import Annotated

from os import getenv
from fastapi import APIRouter, Depends, HTTPException, status
from dotenv import load_dotenv
from .auth import authenticate_user, create_access_token, refresh_token_user, create_refresh_token, user_password_hash, get_current_active_user
from .schemas import TokenResponse, RefreshTokenRequestForm, AccessTokenRequestForm, EmployeeRegistrationForm, EmployeeRegistrationResponse

from sqlalchemy.orm import Session
from ..db import get_db
from ..db.repos import EmployeeRepository
from ..db.schemas.employee import EmployeeInput, EmployeeOutput

load_dotenv("./app/cfg/auth.env")

ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@auth_router.post("/registration", response_model=EmployeeRegistrationResponse)
async def new_user(
    data: EmployeeRegistrationForm,
    user: Annotated[EmployeeOutput, Depends(get_current_active_user)],
    session: Session = Depends(get_db)
):
    new_user = EmployeeInput(
        **data.model_dump()
    )
    
    user = EmployeeRepository(session).create(await user_password_hash(new_user))
    return EmployeeRegistrationResponse(
        id=user.id,
        name=user.name,
        last_name=user.last_name
    )

@auth_router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: AccessTokenRequestForm,
    session: Session = Depends(get_db)
) -> TokenResponse:
    user = await authenticate_user(form_data.firstname, form_data.lastname, form_data.patronymic, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"Authorization": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": str(user.id), "password": user.password}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(user, session)
    return TokenResponse(id=user.id, access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh_access_token(
    form_data: RefreshTokenRequestForm,
    session: Session = Depends(get_db)
) -> TokenResponse:
    user = await refresh_token_user(form_data.id, form_data.refresh_token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or refresh_token",
            headers={"Authorization": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": str(user.id), "password": user.password}, expires_delta=access_token_expires
    )
    refresh_token = await create_refresh_token(user, session)
    return TokenResponse(id=user.id, access_token=access_token, refresh_token=refresh_token, token_type="bearer")