from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.Chat.chat_db_operations import get_chats_by_userid_db, get_chat_history_db, create_chat_db, \
    get_all_chats_db, get_filtered_chats_db
from DataBase.Chat.chat_schemas import ChatCreate, ChatSearch

from DataBase.System.system_db_operations import auth_system_db
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/create_chat")
async def create_chat(new_chat: ChatCreate,
                      request: Request,
                      response: Response,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        system_token = request.cookies.get("system_token")
        response_data = await auth_system_db(system_token, session)
        if response_data == None:
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized system"}


        chat_id = await create_chat_db(new_chat, response_data['id'], session)
        return {"status": "success", "chat_id": chat_id}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/get_chats_by_userid/{user_id}")
async def get_chats_by_userid(user_id: int,
                              request: Request,
                              response: Response,
                              session: AsyncSession = Depends(get_async_session)):
    system_token = request.cookies.get("system_token")
    if await auth_system_db(system_token, session):
        try:
            answer = await get_chats_by_userid_db(user_id, session)
            return {"status": "success", "data": answer}
        except Exception as e:
            response.status_code = 500
            return {"status": "error", "message": str(e)}
    else:
        response.status_code = 400
        return {"status": "error", "message": "Wrong token"}


@router.get("/get_chat_history/{chat_id}")
async def get_chat_history(chat_id: int,
                           page_number: int,
                           page_size: int,
                           request: Request,
                           response: Response,
                           session: AsyncSession = Depends(get_async_session)):
    access = False

    system_token = request.cookies.get("system_token")
    access_token = request.cookies.get("access_token")
    if await auth_system_db(system_token, session) != None or \
            await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
        access = True

    if not access:
        response.status_code = 400
        return {"status": "error", "message": "Unauthorized"}

    try:
        answer = await get_chat_history_db(chat_id, page_number, page_size, session)
        return answer
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}

@router.get("/get_all_chats")
async def get_all_chats(response: Response,
                        request: Request,
                        session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}
        chats_list = await get_all_chats_db(session)
        return {"data": chats_list}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/get_filtered_chats")
async def get_filtered_chats(cur_chat: ChatSearch,
                             response: Response,
                             request: Request,
                             session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}
        chats_list = await get_filtered_chats_db(cur_chat, session)
        return {"data": chats_list}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}
