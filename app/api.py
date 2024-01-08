import aiohttp
from fastapi import FastAPI

from app.models.Body import Body
from app.parsers.tass_parser import get_tass_articles
from config.settings_parser import LIMIT_HOST, TIMEOUT
from app.parsers.rbk_parser import get_rbk_articles


app = FastAPI()


# TODO: Нужно обрабатывать даты если дата окончание меньше даты начала
@app.get("/get-articles")
async def get_articles(body: Body):
    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        return await get_tass_articles(body.start_date, body.end_date, session) + await get_rbk_articles(body.start_date, body.end_date, session)
