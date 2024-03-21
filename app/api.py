# import aiohttp
from fastapi import FastAPI

from app.models.Body import Body
from app.services.data_collection.collect_articles import collect_articles
from app.services.data_processing.preprocess_articles import preprocess_articles

# from app.services.data_collection.parser.tass_parser import get_tass_articles
# from config.settings_parser import LIMIT_HOST, TIMEOUT
# from app.services.data_collection.parser.rbk_parser import get_rbk_articles
# from app.services.data_collection.yahofin import get_currency_history

app = FastAPI()


# TODO: Нужно обрабатывать даты если дата окончание меньше даты начала
@app.get("/get-articles-by-period")
async def get_articles_by_period(body: Body):
    return await collect_articles(body.start_date, body.end_date)

    # connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    # timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    # history_curs = get_currency_history(start_date=body.start_date, end_date=body.end_date)
    # async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
    #     data_articles = await get_tass_articles(body.start_date, body.end_date, session, history_curs) + await get_rbk_articles(
    #         body.start_date, body.end_date, session, history_curs)
    #     return data_articles


@app.get("/get-data-processing")
async def get_data_processing(body: Body):
    data_articles = await collect_articles(body.start_date, body.end_date)
    return preprocess_articles(data_articles)
