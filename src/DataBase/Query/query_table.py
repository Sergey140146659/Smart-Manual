from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from DataBase.Chat.chat_table import chat

metadata = MetaData()

query = Table(
    "query",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("chat_id", Integer, ForeignKey(chat.c.id)),
    Column("query", String),
    Column("result", String),
    Column("comment", String),
    Column("is_valid", Boolean),
    Column("useful_faq", Boolean),
    Column("useful_article", Boolean),
    Column("useful_law", Boolean),
    Column("fixed", Boolean),
    Column("date", TIMESTAMP(timezone=True)),
)
