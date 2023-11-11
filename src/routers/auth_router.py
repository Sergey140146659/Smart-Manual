from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.User.user_schemas import UserLogin
from DataBase.database_config import get_async_session
from fastapi.responses import Response
from DataBase.User.auth_db_operations import login_check, encode_jwt
from config import SECRET_AUTH

import json

JWT_SECRET = SECRET_AUTH
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 120

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(user_login: UserLogin,
                response: Response,
                session: AsyncSession = Depends(get_async_session)):
    return True


@router.post("/logout")
async def logout(response: Response):
    return True
