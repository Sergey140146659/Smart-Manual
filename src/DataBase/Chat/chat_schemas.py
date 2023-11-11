from typing import Optional

from pydantic import BaseModel


class ChatCreate(BaseModel):
    sessionId: int
    userId: int
    isAnonymous: bool
    name: str


class ChatSearch(BaseModel):
    id: Optional[int] = None
    systemId: Optional[int] = None
    sessionId: Optional[int] = None
    userId: Optional[int] = None
    isAnonymous: Optional[bool] = None
    name: Optional[str] = None
