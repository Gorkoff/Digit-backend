from fastapi import FastAPI
from app.models.Body import Body
from app.parser.tass_parser import get_response


app = FastAPI()


# TODO: Нужно обрабатывать даты если дата окончание меньше даты начала
@app.get("/get-articles")
async def get_articles(body: Body):
    return await get_response(body.start_date, body.end_date)

