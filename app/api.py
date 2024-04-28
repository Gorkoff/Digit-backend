from fastapi import FastAPI

from app.models.Body import Body
from app.services.data_collection.collect_articles import collect_articles
from app.services.data_processing.preprocess_articles import preprocess_articles

app = FastAPI()


@app.get("/get-articles-by-period")
async def get_articles_by_period(body: Body):
    return await collect_articles(body.start_date, body.end_date)


@app.get("/get-data-processing")
async def get_data_processing(body: Body):
    data_articles = await collect_articles(body.start_date, body.end_date)
    return preprocess_articles(data_articles)
