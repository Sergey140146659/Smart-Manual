from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/pages",
    tags=["Page"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/search")
def get_search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@router.get("/files")
def get_files_page(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})


@router.get("/admin")
def redirect_to_db_upload():
    return RedirectResponse(url="/pages/admin_db_upload")


@router.get("/admin_notes")
def get_admin_systems_page(request: Request):
    return templates.TemplateResponse("notes.html", {"request": request})


@router.get("/admin_db_upload")
def get_db_upload_page(request: Request):
    return templates.TemplateResponse("db_upload.html", {"request": request})
