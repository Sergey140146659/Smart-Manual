from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func, delete

from DataBase.Chat.chat_schemas import ChatCreate, ChatSearch
from DataBase.Chat.chat_table import chat
from DataBase.Query.query_table import query
from DataBase.database_config import get_async_session


async def get_all_chats_db(session: AsyncSession = Depends(get_async_session)):
    query = select(chat)
    result = await session.execute(query)
    mappings = result.mappings().all()
    return mappings if mappings else None


async def get_filtered_chats_db(search_params: ChatSearch,
                                session: AsyncSession):
    query = select(chat)

    if search_params.id is not None:
        query = query.where(chat.c.id == search_params.id)

    if search_params.systemId is not None:
        query = query.where(chat.c.systemId == search_params.systemId)

    if search_params.sessionId is not None:
        query = query.where(chat.c.sessionId == search_params.sessionId)

    if search_params.userId is not None:
        query = query.where(chat.c.userId == search_params.userId)

    if search_params.isAnonymous is not None:
        query = query.where(chat.c.isAnonymous == search_params.isAnonymous)

    if search_params.name is not None:
        query = query.where(chat.c.name == search_params.name)

    result = await session.execute(query)
    chats = result.mappings().all()
    return chats if chats else None


async def create_chat_db(new_chat: ChatCreate,
                         system_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    new_chat_dict = new_chat.dict()
    new_chat_dict["systemId"] = system_id
    stmt = insert(chat).values(**new_chat_dict)
    result = await session.execute(stmt)
    await session.commit()
    chat_id = result.inserted_primary_key[0]
    return chat_id


async def get_chats_by_userid_db(user_id: int,
                                 session: AsyncSession = Depends(get_async_session)):
    stmt = select(chat).where(user_id == chat.c.userId)
    result = await session.execute(stmt)
    mappings = result.mappings().fetchall()
    return mappings


async def get_chat_history_db(chat_id: int,
                              page_number: int,
                              page_size: int,
                              session: AsyncSession = Depends(get_async_session)):
    stmt = select(query).limit(page_size).offset((page_number - 1) * page_size).where(
        chat_id == query.c.chat_id).order_by(query.c.id.desc())
    result = await session.execute(stmt)
    mappings = result.mappings().fetchall()

    total_stmt = select(func.count()).where(chat_id == query.c.chat_id)
    total_result = await session.execute(total_stmt)
    total_count = total_result.scalar()

    return {"total_count": total_count, "query_list": mappings}


async def delete_chat_db(chat_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    stmt = delete(chat).where(chat.c.id == chat_id)
    await session.execute(stmt)
    await session.commit()
