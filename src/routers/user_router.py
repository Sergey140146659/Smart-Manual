from fastapi import APIRouter, Depends
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.User.user_db_operations import get_all_users_db, delete_user_by_id, find_user_by_id, \
     create_user, update_user, get_user_me, is_active_user
from DataBase.User.user_schemas import UserCreate, UserUpdate
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/create_user")
async def create_new_user(user: UserCreate,
                          request: Request,
                          response: Response,
                          session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        token_id = int(request.cookies.get("token_id"))

        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or \
                not await is_active_user(token_id, session):
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized user"}

        return await create_user(user, session)

    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.delete("/delete_user/{user_id}")
async def delete_users(user_id: int,
                       request: Request,
                       response: Response,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        token_id = int(request.cookies.get("token_id"))

        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or \
                not await is_active_user(token_id, session):
            response.status_code = 400
            return {"status": "Unauthorized user."}

        return await delete_user_by_id(user_id, session)

    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/update_user/{user_id}")
async def update_users(user: UserUpdate,
                       user_id: int,
                       request: Request,
                       response: Response,
                       session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        token_id = int(request.cookies.get("token_id"))

        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or not is_active_user(token_id, session):
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized user"}

        return await update_user(user, user_id, session)

    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/get_all_users")
async def get_all_users(request: Request,
                        response: Response,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        token_id = int(request.cookies.get("token_id"))

        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or not is_active_user(token_id, session):
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized user"}

        users = await get_all_users_db(session)

        return {"status": "success", "data": users}

    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/find_user/{id}")
async def get_user_by_id(user_id: int, request: Request, response: Response, session: AsyncSession = Depends(get_async_session)):
    access_token = request.cookies.get("access_token")
    token_id = int(request.cookies.get("token_id"))
    if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or is_active_user(token_id, session):
        response.status_code = 400
        return {"status": "error", "message": "Unauthorized user"}
    return await find_user_by_id(user_id, session)


@router.get("/get_me")
async def get_me(request: Request,
                 response: Response,
                 session: AsyncSession = Depends(get_async_session)):
    access_token = request.cookies.get("access_token")
    token_id = request.cookies.get("token_id")
    if (not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM)) or len(token_id) == 0:
        response.status_code = 400
        return {"status": "error", "message": "Unauthorized user"}
    token_id = int(token_id)
    return await get_user_me(token_id, session)
