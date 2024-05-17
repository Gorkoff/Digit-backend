from fastapi import FastAPI, Depends

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Body import Body
from app.services.data_base.data_base import get_session
from app.services.data_collection.collect_articles import collect_articles
from app.services.data_collection.parser.parsers import save_articles_to_db, fetch_articles_from_db
from app.services.data_processing.preprocess_articles import preprocess_articles
from app.services.data_clustering.data_clustering import convert_to_json, clusterize_articles
from app.services.data_collection.parser.rbk_parser import get_rbk_articles
from app.services.data_collection.parser.tass_parser import get_tass_articles

app = FastAPI()


@app.get("/get-articles-by-period")
async def get_articles_by_period(body: Body):
    return await collect_articles(body.start_date, body.end_date)


@app.get("/get-data-processing")
async def get_data_processing(body: Body):
    data_articles = await collect_articles(body.start_date, body.end_date)
    return preprocess_articles(data_articles)


@app.get("/get-data-clustering")
async def get_data_clustering(body: Body):
    start_date, end_date = body.start_date, body.end_date
    data_articles = await collect_articles(start_date, end_date)
    df = pd.DataFrame(data_articles)
    # Переделать названия
    return convert_to_json(clusterize_articles(df))


@app.post("/add-articles/")
async def add_articles(start_date: str, end_date: str, session: AsyncSession = Depends(get_session)):
    db_articles = await fetch_articles_from_db(session, start_date, end_date)
    if db_articles:
        return {"status": "success", "articles": db_articles}

    rbk_articles = await get_rbk_articles(start_date, end_date, session, history_curs={})
    tass_articles = await get_tass_articles(start_date, end_date, session, history_curs={})
    articles = rbk_articles + tass_articles

    if articles:
        await save_articles_to_db(session, articles)
        return {"status": "success", "articles": articles}
    else:
        return {"status": "fail", "error": "No articles found"}
