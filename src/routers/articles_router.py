import json
import pickle
from datetime import datetime

import pytz
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.Query.query_schemas import QueryCreate
from DataBase.Query.rate_schemas import Rate, WriteQuestions, IsUseful
from ml.preprocessing_data.Articles_path import get_path
from ml.searching.question_list import get_question_list, update_question_list

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
    try:

        question_list = get_question_list(article_name)
        return question_list
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}




@router.post("/write_questions")
async def post_rate(new_write: WriteQuestions,
                    request: Request,
                    response: Response):
    try:
        update_question_list(new_write.article_name, new_write.query_list)
        return {"status": "success"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}
