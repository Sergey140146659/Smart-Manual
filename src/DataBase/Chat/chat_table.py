from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey

from DataBase.System.system_table import system

metadata = MetaData()

chat = Table(
    "chat",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("systemId", Integer, ForeignKey(system.c.id), nullable=False),
    Column("userId", Integer, nullable=True),
    Column("isAnonymous", Boolean, nullable=False),
    Column("sessionId", Integer, nullable=True),
    Column("name", String),
)
