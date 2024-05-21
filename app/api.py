from fastapi import FastAPI, Depends, HTTPException
import pandas as pd
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.Body import Body
from app.services.data_base.data_base import get_session
from app.services.data_collection.collect_articles import collect_articles
from app.services.data_collection.parser.parsers import save_articles_to_db
from app.services.data_processing.preprocess_articles import preprocess_articles
from app.services.data_clustering.data_clustering import convert_to_json, clusterize_articles

from sqlalchemy.sql import text

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


@app.post("/add-articles")
async def add_articles(body: Body, session: AsyncSession = Depends(get_session)):
    async with session.begin():  # Явное начало транзакции
        try:
            start_date = datetime.strptime(body.start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(body.end_date, '%Y-%m-%d').date()

            query = text("SELECT * FROM public.article WHERE published_dt BETWEEN :start_date AND :end_date")
            result = await session.execute(query, {'start_date': start_date, 'end_date': end_date})
            existing_articles = result.scalars().all()

            if existing_articles:
                return {"status": "success", "message": "Articles already exist in the database", "articles": existing_articles}

            articles = await collect_articles(body.start_date, body.end_date)
            if not articles:
                return {"status": "fail", "error": "No new articles found"}

            await save_articles_to_db(session, articles)
            await session.commit()
            return {"status": "success", "message": "New articles added", "articles": articles}

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Error processing your request: {str(e)}")
