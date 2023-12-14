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

# TODO: Обработка ошибок сервера

async def get_responce(start, end, max_concurrent_requests=10):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    result = []
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with aiohttp.ClientSession() as session:
        generator = list(date_generator(start_date, end_date))
        tasks = [fetch_data(session, date, semaphore) for date in generator]
        responses = await asyncio.gather(*tasks)

        parse_tasks = []
        article_metadata = []
        for articles in responses:
            for article in articles.get('result'):
                url = f"https://tass.ru{article.get('url')}"
                parse_tasks.append(scrape(session, url))
                article_metadata.append({
                    'title': article.get('title'),
                    'url': url,
                    'published_dt': datetime.fromisoformat(article.get('published_dt')).strftime('%Y-%m-%d'),
                    'tags': [tag.get('name') for tag in article.get('tags')]
                })
        parsed_texts = await asyncio.gather(*parse_tasks)

        for metadata, text in zip(article_metadata, parsed_texts):
            metadata['text'] = text
            result.append(metadata)

    return result


async def fetch_data(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as response:
            await asyncio.sleep(1)
            return await response.json()
