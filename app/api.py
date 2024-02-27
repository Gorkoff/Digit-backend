import aiohttp
from fastapi import FastAPI

from app.models.Body import Body
from app.parsers.tass_parser import get_tass_articles
from config.settings_parser import LIMIT_HOST, TIMEOUT
from app.parsers.rbk_parser import get_rbk_articles
from app.services.yahofin import get_currency_history

app = FastAPI()


# TODO: Нужно обрабатывать даты если дата окончание меньше даты начала
@app.get("/get-articles")
async def get_articles(body: Body):
    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    history_curs = get_currency_history(start_date=body.start_date, end_date=body.end_date)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        data_articles = await get_tass_articles(body.start_date, body.end_date, session, history_curs) + await get_rbk_articles(
            body.start_date, body.end_date, session, history_curs)
        predproc(data_articles)
        return data_articles
