from fastapi import File, UploadFile, APIRouter, Form

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)


@router.post("/subject_db_upload")
async def subject_db_upload(subject: str = Form(...), subject_file: UploadFile = File(...)):
    print({"filename": subject_file.filename, "subject": subject})
    return {"filename": subject_file.filename, "subject": subject}