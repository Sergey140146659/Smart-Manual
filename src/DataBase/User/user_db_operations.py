from http.client import HTTPException
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func

from DataBase.database_config import get_async_session
from fastapi import Depends, Response
from DataBase.User.user_schemas import UserCreate, UserUpdate
from DataBase.User.user_table import User
from passlib.context import CryptContext


async def get_all_users_db(session: AsyncSession = Depends(get_async_session)):
    try:
        user = select(User)
        result = await session.execute(user)
        mappings = result.mappings().all()
        return mappings if mappings else None
    except Exception as e:
        return {"status": "failed", "message": str(e)}


async def is_active_user(user_id: int,
                         session: AsyncSession = Depends(get_async_session)) -> bool:
    if user_id is None:
        return False
    user = select(User).where(User.id == user_id)
    result = await session.execute(user)
    user_is = result.scalars().first()
    return user_is.is_superuser


async def delete_user_by_id(user_id,
                            session: AsyncSession = Depends(get_async_session)):
    try:
        user = select(User).where(User.id == user_id)
        result = await session.execute(user)
        user_to_delete = result.scalars().first()
        if not user_to_delete:
            return {"status": "failed", "message": f"User with id {user_id} not found"}
        await session.delete(user_to_delete)
        await session.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


async def find_user_by_id(user_id, session: AsyncSession = Depends(get_async_session)):
    try:
        user = select(User).where(User.id == user_id)
        result = await session.execute(user)
        db_user = result.fetchone()
        if db_user:
            return db_user._asdict()
        else:
            return {"status": "failed", "message": f"User with id {user_id} not found"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


async def create_user(user: UserCreate,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        check_user = select(User).where(User.email == user.email)
        result = await session.execute(check_user)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return {"status": "This user is already registered"}
        new_user = User(email=user.email,
                        username=user.username,
                        hashed_password=hash_password(user.password),
                        is_active=user.is_active,
                        is_superuser=user.is_superuser,
                        is_verified=user.is_verified)
        session.add(new_user)
        await session.commit()
        return new_user

    except Exception as e:
        return {"status": "failed", "message": str(e)}


async def update_user(user: UserUpdate,
                      user_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        db_user = await session.get(User, user_id)
        if db_user is None:
            return None
        for field, value in user.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        await session.commit()
        return db_user

    except Exception as e:
        return {"status": "failed", "message": str(e)}


def get_user_response(response: Response = Depends()):
    return response


async def get_user_me(token_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        if token_id is None:
            return {"status": "failed", "message": "error 401, ну войди в систему пожаааааалуйста)"}
        db_user = await session.get(User, token_id)
        if db_user:
            return db_user
        else:
            return {"status": "failed", "message": "User not found"}
    except Exception as e:

        return {"status": "failed", "message": str(e)}


def get_user_response(response: Response = Depends()):
    return response


# Password hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
