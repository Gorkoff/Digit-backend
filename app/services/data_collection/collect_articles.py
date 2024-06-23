import aiohttp
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from config.settings_parser import LIMIT_HOST, TIMEOUT
from app.services.data_collection.parser.tass_parser import get_tass_articles
from app.services.data_collection.parser.rbk_parser import get_rbk_articles
from app.services.data_collection.yahofin import get_currency_history
from app.services.data_collection.parser.parsers import save_articles_to_db


async def collect_articles(start_date: str, end_date: str, session: AsyncSession):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)

    # Запрос для получения статей из базы данных
    async with session.begin():
        query = text("SELECT * FROM public.article WHERE published_dt BETWEEN :start_date AND :end_date")
        result = await session.execute(query, {'start_date': start_date_dt, 'end_date': end_date_dt})
        existing_articles = result.fetchall()

    def article_to_dict(article):
        return {
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "published_dt": article.published_dt.isoformat() if article.published_dt else None,
            "currency_curs": article.currency_curs,
            "text": article.text
        }

    existing_articles_dict = [article_to_dict(article) for article in existing_articles]

    # Если все статьи за период уже существуют в базе данных
    existing_dates = {article['published_dt'][:10] for article in existing_articles_dict}
    all_dates = {(start_date_dt + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date_dt - start_date_dt).days + 1)}
    missing_dates = all_dates - existing_dates

    if not missing_dates:
        return {"status": "success", "message": "Articles already exist in the database", "articles": existing_articles_dict}

    # Преобразование недостающих дат в строки
    missing_start_date = min(missing_dates)
    missing_end_date = max(missing_dates)

    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    history_curs = get_currency_history(start_date=missing_start_date, end_date=missing_end_date)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as http_session:
        tass_articles = await get_tass_articles(missing_start_date, missing_end_date, http_session, history_curs)
        rbk_articles = await get_rbk_articles(missing_start_date, missing_end_date, http_session, history_curs)
        new_articles = tass_articles + rbk_articles

        if new_articles:
            async with session.begin():
                await save_articles_to_db(session, new_articles)
                await session.commit()

            # Получаем все статьи заново из базы данных после добавления новых статей
            async with session.begin():
                result = await session.execute(query, {'start_date': start_date_dt, 'end_date': end_date_dt})
                existing_articles = result.fetchall()
                existing_articles_dict = [article_to_dict(article) for article in existing_articles]

            return {"status": "success", "message": "New articles added", "articles": existing_articles_dict}

    # Если не удалось найти и добавить новые статьи
    return {"status": "fail", "error": "No new articles found and some dates are missing in the database"}

# def articles_to_dataframe(start_date, end_date):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     data = loop.run_until_complete(collect_articles(start_date, end_date))
#     df = pd.DataFrame(data)
#     return df
