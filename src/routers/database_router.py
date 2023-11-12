from fastapi import File, UploadFile, APIRouter, Form

from ml.db_creating.create_subject import create_subject
from ml.db_creating.subject_list import get_subject_list
from ml.preprocessing_data.Articles_path import get_path

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)


@router.post("/subject_db_upload")
async def subject_db_upload(subject: str = Form(...), subject_file: UploadFile = File(...)):
    file_path = get_path(subject_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await subject_file.read())
    obj = {"name": subject, "themes": [], "path": subject_file.filename}
    create_subject(obj)
    return {"status": "ok"}


@router.get("/subject_list")
async def subject_list():
    return get_subject_list()
