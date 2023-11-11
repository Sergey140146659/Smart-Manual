from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/pages",
    tags=["Page"]
)

templates = Jinja2Templates(directory="templates")

async def check_authentication(request: Request):
   return True


@router.get("/chatbot")
def get_chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})

@router.get("/admin_bot_rate")
def get_admin_bot_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_bot_rate.html", {"request": request})

@router.get("/admin_rates")
def get_admin_systems_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_rates.html", {"request": request})

@router.get("/admin_systems")
def get_admin_systems_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_systems.html", {"request": request})

@router.get("/admin_chats")
def get_admin_chats_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_chats.html", {"request": request})

@router.get("/admin_queries")
def get_admin_chats_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_queries.html", {"request": request})

@router.get("/admin_users")
def get_user_list_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_users.html", {"request": request})

@router.get("/admin_db_upload")
def get_db_upload_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_db_upload.html", {"request": request})

@router.get("/admin_stats")
def get_admin_stats_page(request: Request, authenticated: bool = Depends(check_authentication)):
    if (not authenticated):
        return RedirectResponse(url="/pages/login")
    return templates.TemplateResponse("admin_statistics.html", {"request": request})

@router.get("/login")
def get_admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})