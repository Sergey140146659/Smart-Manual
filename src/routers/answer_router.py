from fastapi import APIRouter, Response, Request

from ml.searching.request_answer import get_answer as get_answer_func

router = APIRouter(
    prefix="/answer",
    tags=["Answer"]
)


@router.get("/get_answer")
async def get_answer(subject_name: str,
                     request: str,
                     response: Response):
    try:
        return get_answer_func(subject_name, request)
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}
