from pydantic import BaseModel


class SystemCreate(BaseModel):
    name: str
    region: str
    system_type_id: int
    bug_tracker: str = None


class SystemAuth(BaseModel):
    system_token: str
