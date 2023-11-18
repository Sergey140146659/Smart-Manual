import json
from typing import List

from fastapi import File, UploadFile, APIRouter, Form, Response

from ml.db_creating.create_subject import create_subject
from ml.db_creating.subject_list import get_subject_list
from ml.preprocessing_data.Articles_path import get_path
from ml.db_creating.view_subject import marked_list
from ml.db_creating.question_mode import get_note, write_note

router = APIRouter(
    prefix="/db",
    tags=["DataBase"]
)


@router.post("/subject_db_upload")
async def subject_db_upload(response: Response,
                            themes: List[str],
                            subject_name: str = Form(...),
                            subject_file: UploadFile = File(...)):
    try:
        themes = json.loads(themes[0])
        for t in themes:
            t['page_start'] = int(t['page_start'])
            t['page_end'] = int(t['page_end'])
        file_path = get_path(subject_file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await subject_file.read())
        obj = {"name": subject_name, "themes": themes, "path": subject_file.filename}
        create_subject(obj)
        return {"status": "ok"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/subject_list")
async def subject_list(response: Response):
    try:
        return get_subject_list()
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/wide_subject_list")
async def wide_subject_list(response: Response):
    try:
        return marked_list()
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/theme_notes")
async def theme_notes(response: Response,
                      subject_name: str,
                      theme_name: str):
    try:
        return get_note(subject_name, theme_name)
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}            


@router.post("/write_theme_notes")
async def write_theme_notes(response: Response,
                            subject_name: str,
                            theme_name: str,
                            note: str):
    try:
        write_note(subject_name, theme_name, note)
        return {"status": "ok"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}