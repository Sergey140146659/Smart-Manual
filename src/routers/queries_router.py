from datetime import datetime

from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.Query.query_db_operations import get_filtered_queries_db, query_set_fixed_db, get_queries_stats_db
from DataBase.Query.query_schemas import QuerySearch
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


@router.post("/get_filtered_queries")
async def filtered_queries(request: Request,
                           response: Response,
                           search_params: QuerySearch,
                           page_size: int,
                           current_page: int,
                           session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}

        queries_list = await get_filtered_queries_db(search_params, page_size, current_page, session)
        return queries_list
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/get_queries_stats")
async def get_queries_stats(request: Request,
                            response: Response,
                            system_id: int, date_start: datetime, date_end: datetime,
                            session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}
        res = await get_queries_stats_db(system_id, date_start, date_end, session)
        return {"status": "success", "data": res}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}



@router.post("/query_set_fixed")
async def query_set_fixed(request: Request,
                          response: Response,
                          query_id: int,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}

        await query_set_fixed_db(query_id, session)
        return {"status": "success"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}