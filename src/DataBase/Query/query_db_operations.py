from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, func

from DataBase.Chat.chat_db_operations import get_filtered_chats_db
from DataBase.Chat.chat_schemas import ChatSearch
from DataBase.Query.query_schemas import QuerySearch
from DataBase.database_config import get_async_session
from DataBase.Query.query_table import query


async def add_query_db(new_query,
                       session: AsyncSession = Depends(get_async_session)):
    stmt = insert(query).values(**new_query)
    result_proxy = await session.execute(stmt)
    query_id = result_proxy.inserted_primary_key[0]
    await session.commit()

    return {"status": "success", "query_id": query_id}


async def query_is_useful_db(new_is_useful,
                             session: AsyncSession = Depends(get_async_session)):
    query_id = new_is_useful.query_id
    query_type = 'useful_' + new_is_useful.answer_type
    useful_rate = new_is_useful.useful_rate

    stmt = update(query).where(query.c.id == query_id).values(**{query_type: useful_rate})
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}


async def get_filtered_queries_db(search_params: QuerySearch,
                                  page_size: int,
                                  current_page: int,
                                  session: AsyncSession = Depends(get_async_session)):
    db_query = select(query)

    if search_params.not_fixed is not None:
        db_query = db_query.where(query.c.fixed == False)

    if search_params.useful_faq is not None:
        db_query = db_query.where(query.c.useful_faq == search_params.useful_faq)

    if search_params.useful_article is not None:
        db_query = db_query.where(query.c.useful_article == search_params.useful_article)

    if search_params.useful_law is not None:
        db_query = db_query.where(query.c.useful_law == search_params.useful_law)

    if search_params.query_include is not None:
        db_query = db_query.where(query.c.query.like(f"%{search_params.query_include}%"))

    if search_params.date_start is not None:
        db_query = db_query.where(query.c.date >= search_params.date_start)

    if search_params.date_end is not None:
        db_query = db_query.where(query.c.date <= search_params.date_end)

    if search_params.chat_id is not None:
        db_query = db_query.where(query.c.chat_id == search_params.chat_id)

    chat_param = ChatSearch()

    if search_params.system_id is not None:
        chat_param.systemId = search_params.system_id

    if search_params.user_id is not None:
        chat_param.userId = search_params.user_id

    if search_params.random is not None:
        db_query = db_query.order_by(func.random())

    chats_list = await get_filtered_chats_db(chat_param, session)
    chat_ids = [chat.id for chat in chats_list]
    db_query = db_query.where(query.c.chat_id.in_(chat_ids))

    db_query = db_query.order_by(query.c.date.desc())

    offset = (current_page - 1) * page_size
    db_query = db_query.limit(page_size).offset(offset)

    result = await session.execute(db_query)
    queries = result.mappings().all()
    return queries if queries else None


async def get_queries_stats_db(system_id: int, date_start: datetime, date_end: datetime,
                               session: AsyncSession = Depends(get_async_session)):
    db_query = select(func.count()).select_from(query)
    db_query = db_query.where(query.c.date >= date_start)
    db_query = db_query.where(query.c.date <= date_end)

    chat_param = ChatSearch()

    if system_id is not None:
        chat_param.systemId = system_id
    chats_list = await get_filtered_chats_db(chat_param, session)
    chat_ids = [chat.id for chat in chats_list]
    db_query = db_query.where(query.c.chat_id.in_(chat_ids))

    result = await session.execute(db_query)

    count = result.scalar()
    return count


async def query_set_fixed_db(query_id,
                             session: AsyncSession = Depends(get_async_session)):

    stmt = update(query).where(query.c.id == query_id).values(fixed=True)
    await session.execute(stmt)
    await session.commit()

    return {"status": "success"}
