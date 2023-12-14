from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.models.Body import Body
from handlers.handler_tass import get_responce

app = FastAPI()


# TODO: Нужно обрабатывать даты если дата окончание меньше даты начала
@app.get("/get-articles")
async def get_articles(body: Body):
    return await get_responce(body.start_date, body.end_date)
