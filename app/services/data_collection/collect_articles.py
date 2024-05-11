import aiohttp
import pandas as pd
import asyncio

from app.services.data_collection.parser.tass_parser import get_tass_articles
from config.settings_parser import LIMIT_HOST, TIMEOUT
from app.services.data_collection.parser.rbk_parser import get_rbk_articles
from app.services.data_collection.yahofin import get_currency_history


async def collect_articles(start_date, end_date):
    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    history_curs = get_currency_history(start_date=start_date, end_date=end_date)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        return await get_tass_articles(start_date, end_date, session, history_curs) + await get_rbk_articles(
            start_date, end_date, session, history_curs)


# def articles_to_dataframe(start_date, end_date):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     data = loop.run_until_complete(collect_articles(start_date, end_date))
#     df = pd.DataFrame(data)
#     return df
