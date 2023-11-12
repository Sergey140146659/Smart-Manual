import pickle

from fastapi import APIRouter, Response, Request

from DataBase.Query.rate_schemas import WriteQuestions
from ml.preprocessing_data.Articles_path import get_path

router = APIRouter(
    prefix="/article",
    tags=["Article"]
)





@router.get("/get_articles_list")
async def get_articles_list(response: Response):
    try:

        with open(get_path('article_list.pkl'), 'rb') as f:
            articles_list = pickle.load(f)

        return articles_list
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/get_faq_list")
async def get_faq_list(response: Response):
    try:

        with open(get_path('faq_list.pkl'), 'rb') as f:
            faq_list = pickle.load(f)

        return faq_list
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.get("/get_article_question_list")
async def get_article_question_list(article_name,
                                    response: Response):
    return 0


@router.post("/write_questions")
async def post_rate(new_write: WriteQuestions,
                    request: Request,
                    response: Response):
    return 0
