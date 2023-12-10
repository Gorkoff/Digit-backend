from datetime import datetime, timedelta
import asyncio
import aiohttp
from app.async_parser import scrape


def date_generator(start_date, end_date, step=1):
    current_date = start_date
    while current_date <= end_date:
        yield f"https://tass.ru/tbp/api/v1/search?limit=20&offset=0&lang=ru&types=news&rubrics=ekonomika&sort" \
              f"=-es_updated_dt&from_date={(current_date - timedelta(days=1)).strftime('%Y-%m-%d')}T23:59:59&to" \
              f"_date={current_date.strftime('%Y-%m-%d')}T23:59:59"

        current_date += timedelta(days=step)


async def get_responce(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    result = []
    async with aiohttp.ClientSession() as session:
        generator = list(date_generator(start_date, end_date))
        tasks = [fetch_data(session, date) for date in generator]
        responses = await asyncio.gather(*tasks)
        for articles in responses:
            for article in articles.get('result'):
                url = f"https://tass.ru{article.get('url')}"
                result.append({
                    'title': article.get('title'),
                    'url': url,
                    'published_dt': datetime.fromisoformat(article.get('published_dt')).strftime('%Y-%m-%d'),
                    "text": await scrape(session, url),
                    "tags": [tag.get('name') for tag in article.get('tags')]
                })
    return result


async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()
