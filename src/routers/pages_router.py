from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/pages",
    tags=["Page"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/chatbot")
def get_chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {"request": request})


@router.get("/admin_rates")
def get_admin_systems_page(request: Request):
    return templates.TemplateResponse("admin_rates.html", {"request": request})


@router.get("/admin_db_upload")
def get_db_upload_page(request: Request):
    return templates.TemplateResponse("admin_db_upload.html", {"request": request})
