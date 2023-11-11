from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

import uuid

metadata = MetaData()

systemType = Table(
    "system_type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
)

system = Table(
    "system",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("token", String),
    Column("region", String),
    Column("system_type_id", Integer, ForeignKey(systemType.c.id)),
    Column("bug_tracker", String, nullable=True),
)
