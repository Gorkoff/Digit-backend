from sqlalchemy.future import select
from sqlalchemy import insert
from app.models.Models_DB import article
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


async def fetch_articles_from_db(session: AsyncSession, start_date: str, end_date: str):
    result = await session.execute(
        select(article).where(article.c.published_dt >= start_date).where(article.c.published_dt <= end_date)
    )
    return result.fetchall()



async def save_articles_to_db(session: AsyncSession, articles):
    formatted_articles = []
    for article_data in articles:
        article_dict = dict(article_data)
        if isinstance(article_dict['published_dt'], datetime):
            print(f"Original published_dt: {article_dict['published_dt']}")  # Отладочный вывод
            article_dict['published_dt'] = article_dict['published_dt'].strftime('%Y-%m-%d')
            print(f"Converted published_dt: {article_dict['published_dt']}")  # Отладочный вывод
        formatted_articles.append(article_dict)

    print(f"Formatted articles: {formatted_articles}")  # Отладочный вывод

    stmt = insert(article).values(formatted_articles)
    await session.execute(stmt)
