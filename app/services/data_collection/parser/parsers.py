from sqlalchemy.future import select
from sqlalchemy import insert
from app.models.Models_DB import article
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_articles_from_db(session: AsyncSession, start_date: str, end_date: str):
    result = await session.execute(
        select(article).where(article.c.published_dt >= start_date).where(article.c.published_dt <= end_date)
    )
    return result.fetchall()


async def save_articles_to_db(session: AsyncSession, articles):
    async with session.begin():
        await session.execute(
            insert(article),
            articles
        )
    await session.commit()