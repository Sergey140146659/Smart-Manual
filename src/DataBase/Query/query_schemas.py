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
