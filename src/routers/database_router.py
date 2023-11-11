import os
import shutil
import time
import zipfile

from fastapi import File, UploadFile, APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.User.user_db_operations import is_active_user
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from ml.db_creating.db_article_update import article_db_update
from ml.db_creating.db_faq_update import faq_db_update
from ml.preprocessing_data.Articles_path import get_path
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)


@router.post("/upload_db")
async def create_upload_file(request: Request,
                             response: Response,
                             file: UploadFile = File(...),
                             session: AsyncSession = Depends(get_async_session)):
    try:
        access_token = request.cookies.get("access_token")
        token_id = int(request.cookies.get("token_id"))

        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM) or \
                not await is_active_user(token_id, session):
            response.status_code = 401
            return {"status": "error", "message": "Unauthorized user."}

        os.makedirs("ml\\preprocessing_data", exist_ok=True)
        if os.path.isdir(get_path("03.complex-operations")):
            shutil.rmtree(get_path("03.complex-operations"))
        if os.path.isdir(get_path("05.f-a-q")):
            shutil.rmtree(get_path("05.f-a-q"))
        file_path = get_path(file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        archive_path = get_path(file.filename)  # путь к архиву
        extract_path = get_path('')
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        shutil.rmtree(get_path('backup'))  # удаляем папку backup

        shutil.move(get_path('user') + '/pages', get_path(''))  # извлекаем папку pages

        shutil.rmtree(get_path('user'))  # удаляем папку user

        folders = [f for f in os.listdir(get_path('pages')) if
                   os.path.isdir(os.path.join(get_path('pages'), f))]  # смотрим все папки из pages

        for folder in folders:
            if "complex-operations" in folder or "f-a-q" in folder:
                shutil.move(get_path('pages') + '/' + folder, get_path(''))  # вытаскиваем complex-operations и f-a-q

        shutil.rmtree(get_path('pages'))  # удаляем папку pages
        os.remove(get_path(file.filename))  # удаляем архив
        article_db_update()
        faq_db_update()

        return {"filename": file.filename}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}
