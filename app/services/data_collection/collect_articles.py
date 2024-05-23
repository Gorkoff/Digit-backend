import aiohttp
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from config.settings_parser import LIMIT_HOST, TIMEOUT
from app.services.data_collection.parser.tass_parser import get_tass_articles
from app.services.data_collection.parser.rbk_parser import get_rbk_articles
from app.services.data_collection.yahofin import get_currency_history
from app.services.data_collection.parser.parsers import save_articles_to_db
from app.models.Body import Body


async def collect_articles(start_date: str, end_date: str, session: AsyncSession):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d').date()

    query = text("SELECT * FROM public.article WHERE published_dt BETWEEN :start_date AND :end_date")
    result = await session.execute(query, {'start_date': start_date_dt, 'end_date': end_date_dt})
    existing_articles = result.scalars().all()

    if existing_articles:
        return {"status": "success", "message": "Articles already exist in the database", "articles": existing_articles}

    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    history_curs = get_currency_history(start_date=start_date, end_date=end_date)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as http_session:
        tass_articles = await get_tass_articles(start_date, end_date, http_session, history_curs)
        rbk_articles = await get_rbk_articles(start_date, end_date, http_session, history_curs)
        new_articles = tass_articles + rbk_articles

        if not new_articles:
            return {"status": "fail", "error": "No new articles found"}

        await save_articles_to_db(session, new_articles)
        await session.commit()
        return {"status": "success", "message": "New articles added", "articles": new_articles}

# def articles_to_dataframe(start_date, end_date):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     data = loop.run_until_complete(collect_articles(start_date, end_date))
#     df = pd.DataFrame(data)
#     return df
