from sqlalchemy import MetaData, Integer, String, Table, Column, VARCHAR, FLOAT, TIMESTAMP, Index, Text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.sql import text
import asyncio
from app.services.data_base.data_base import database_engine
from app.services.data_base.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

metadata = MetaData()

database_engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", VARCHAR(256)),
    Column("url", VARCHAR(128)),
    Column("published_dt", TIMESTAMP),
    Column("currency_curs", FLOAT),
    Column("text", Text),
)

# Кластеризованный индекс (для PostgreSQL нужно будет использовать `postgresql_using='cluster'` в create_engine)
index = Index('ix_published_dt', article.c.published_dt)


# Асинхронная функция для создания таблицы и индекса
async def create_tables_and_cluster():
    async with database_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    # Выполнение команды CLUSTER отдельно
    async with database_engine.connect() as conn:
        await conn.execute(text("CLUSTER article USING ix_published_dt"))

# Вызов асинхронной функции
asyncio.run(create_tables_and_cluster())
