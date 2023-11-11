import uuid

from fastapi import Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.System.system_schemas import SystemCreate
from DataBase.System.system_table import system, systemType
from DataBase.database_config import get_async_session


async def get_all_systems_db(session: AsyncSession = Depends(get_async_session)):
    query = select(system)
    result = await session.execute(query)
    mappings = result.mappings().all()
    return mappings if mappings else None


async def get_system_types(system_id: int,
                           system_name: str,
                           session: AsyncSession = Depends(get_async_session)):
    try:

        stmt = insert(systemType).values(**{"id": system_id, "name": system_name})
        await session.execute(stmt)
        await session.commit()
        return {"status": "Успех"}

    except Exception as e:
        return {"status": "failed", "message": str(e)}


async def add_system_db(new_system: SystemCreate,
                        session: AsyncSession = Depends(get_async_session)):
    new_system_dict = new_system.dict()
    new_system_dict["token"] = str(uuid.uuid4())
    stmt = insert(system).values(**new_system_dict)
    await session.execute(stmt)
    await session.commit()

    query = select(system).where(system.c.name == new_system.dict()["name"])

    result = await session.execute(query)
    mappings = result.mappings().first()
    return mappings["token"]


async def auth_system_db(system_token: str,
                         session: AsyncSession = Depends(get_async_session)):
    return True


async def delete_system_db(system_id: int,
                           session: AsyncSession = Depends(get_async_session)):
    stmt = delete(system).where(system.c.id == system_id)
    await session.execute(stmt)
    await session.commit()
