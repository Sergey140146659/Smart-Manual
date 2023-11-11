import json
import pickle
from datetime import datetime

import pytz
from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.Query.query_schemas import QueryCreate
from DataBase.Query.rate_schemas import Rate, WriteQuestions, IsUseful
from DataBase.database_config import get_async_session
from auth.auth_config import validate_token
from ml.db_creating.db_correction import add_question as add_question_db
from ml.preprocessing_data.Articles_path import get_path
from ml.searching.question_list import get_question_list, update_question_list
from ml.searching.request_answer import answer_user_question as ml_user_get_answer, get_answer
from routers.auth_router import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/article",
    tags=["Article"]
)


@router.post("/get_answer")
async def answer(new_query: QueryCreate,
                 request: Request,
                 response: Response,
                 session: AsyncSession = Depends(get_async_session)):
    try:
        questions = new_query.questions
        questions_dict = questions.__dict__

        query_answer = ml_user_get_answer(new_query.query, questions_dict)

        return {"status": "success", "data": query_answer}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/get_answer_without_classification")
async def answer_without_classification(new_query: QueryCreate,
                                        request: Request,
                                        response: Response,
                                        session: AsyncSession = Depends(get_async_session)):
    try:
        questions = new_query.questions
        questions_dict = questions.__dict__
        query_answer = get_answer(new_query.query, questions_dict)
        return {"status": "success", "data": query_answer}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


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


@router.post("/add_question")
async def add_question(new_rate: Rate,
                       request: Request,
                       response: Response):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized user."}

        add_question_db([{
            "article_name": new_rate.article_name,
            "query": new_rate.query
        }])
        return {"status": "success"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}


@router.post("/write_questions")
async def post_rate(new_write: WriteQuestions,
                    request: Request,
                    response: Response):
    try:
        access_token = request.cookies.get("access_token")
        if not await validate_token(access_token, JWT_SECRET, JWT_ALGORITHM):
            response.status_code = 400
            return {"status": "error", "message": "Unauthorized user."}

        update_question_list(new_write.article_name, new_write.query_list)
        return {"status": "success"}
    except Exception as e:
        response.status_code = 500
        return {"status": "error", "message": str(e)}
