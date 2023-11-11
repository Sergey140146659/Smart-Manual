from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from DataBase.System.system_db_operations import add_system_db, delete_system_db, auth_system_db, get_all_systems_db, \
    get_system_types
from DataBase.System.system_schemas import SystemCreate, SystemAuth
from DataBase.User.user_db_operations import is_active_user
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/system",
    tags=["System"]
)


@router.post("/add_system")
async def add_system(new_system: SystemCreate,
                     response: Response,
                     request: Request,
                     session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            return {"status": "Unauthorized user."}
        access_token = await add_system_db(new_system, session)
        return {"access_token": access_token}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/auth_system")
async def login(auth_system: SystemAuth,
                response: Response,
                session: AsyncSession = Depends(get_async_session)):
    system_token = auth_system.system_token
    response.headers["system_token"] = auth_system.system_token
    if await auth_system_db(system_token, session):
        try:
            response.set_cookie(key="system_token", value=system_token)
            return {"status": "success", "message": "Logged in successfully"}
        except Exception as e:
            response.status_code = 500
            return {"status": "error", "message": str(e)}
    else:
        response.status_code = 400
        return {"status": "error", "message": "Wrong token"}


@router.get("/get_all_systems")
async def get_all_systems(response: Response,
                          request: Request,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}
        systems_list = await get_all_systems_db(session)
        return {"data": systems_list}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/add_system_type")
async def add_system_type(response: Response,
                          request: Request,
                          system_id: int,
                          system_name: str,
                          session: AsyncSession = Depends((get_async_session))):
    access_token = request.cookies.get("access_token")
    token_id = int(request.cookies.get("token_id"))

    if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or (
            not await is_active_user(token_id, session)):
        response.status_code = 401
        return {"status": "error", "message": "Unauthorized user."}
    return await get_system_types(system_id, system_name, session)
