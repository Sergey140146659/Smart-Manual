from typing import List, Optional

from pydantic import BaseModel

class Rate(BaseModel):
    query: str
    article_name: str


class WriteQuestions(BaseModel):
    article_name: str
    query_list: List[str]


class IsUseful(BaseModel):
    query_id: int
    answer_type: str
    useful_rate: bool
