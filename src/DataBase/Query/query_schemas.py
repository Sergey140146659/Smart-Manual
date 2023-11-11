from datetime import datetime
from typing import Optional

import pytz
from pydantic import BaseModel


class Questions(BaseModel):
    faq: bool = True
    article: bool = True
    law: bool = True


class QueryCreate(BaseModel):
    chat_id: int
    query: str
    questions: Optional[Questions] = Questions()


class QuerySearch(BaseModel):
    useful_faq: Optional[bool] = None
    useful_article: Optional[bool] = None
    useful_law: Optional[bool] = None
    query_include: Optional[str] = None
    chat_id: Optional[int] = None
    user_id: Optional[int] = None
    system_id: Optional[int] = None
    not_fixed: Optional[bool] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    random: Optional[bool] = None
