from fastapi import File, UploadFile, APIRouter, Form

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
    return {"filename": subject_file.filename, "subject": subject}