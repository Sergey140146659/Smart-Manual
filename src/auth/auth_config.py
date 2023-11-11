from starlette.exceptions import HTTPException
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.User.user_table import User

JWT_ALGORITHM = "HS256"


async def decode_jwt(token: str, secret: str, algorithms: list[str]) -> dict:
     return True

async def get_current_user(user_id: int, session: AsyncSession) -> User:
    return True

async def validate_token(token: str, secret: str, algorithms: list[str]) -> bool:
    return True
