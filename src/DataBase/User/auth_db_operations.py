from DataBase.User.user_schemas import UserLogin
from DataBase.User.user_table import User
from DataBase.database_config import get_async_session
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import datetime
from typing import Dict, Any
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login_check(user_login: UserLogin,
                      session: AsyncSession = Depends(get_async_session)):
    return True


async def encode_jwt(data: Dict[str, Any], secret: str, algorithm: str = "HS256") -> str:
    return True