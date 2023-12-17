from datetime import datetime, timedelta
import asyncio
import aiohttp
import random
from app.services.async_parser import scrape
from app.services.yahofin import get_currency_history


def date_generator(start_date, end_date, step_hours=24):
    current_date = start_date
    while current_date <= end_date:
        yield f"https://tass.ru/tbp/api/v1/search?limit=20&offset=0&lang=ru&types=news&rubrics=mezhdunarodnaya" \
              f"-panorama&rubrics=ekonomika&sort=-es_updated_dt&from_date={current_date.isoformat()}&to" \
              f"_date={(current_date + timedelta(hours=step_hours)).isoformat()}"
        current_date += timedelta(hours=step_hours)


async def get_response(start, end, max_concurrent_requests=5):
    """ Асинхронный запрос к API для получения данных. """
    history_curs = get_currency_history(start_date=start, end_date=end)
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    semaphore = asyncio.Semaphore(max_concurrent_requests)
    connector = aiohttp.TCPConnector(limit_per_host=5)
    timeout = aiohttp.ClientTimeout(total=180)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        fetch_tasks = [safe_fetch(session, url, semaphore) for url in date_generator(start_date, end_date)]
        responses = await asyncio.gather(*fetch_tasks, return_exceptions=True)
        parse_tasks = []
        article_metadata = []
        result = []
        for response in responses:
            for article in response.get('result', []):
                url = f"https://tass.ru{article.get('url', '')}"
                published_dt = datetime.fromisoformat(article.get('published_dt')).strftime('%Y-%m-%d')
                parse_tasks.append(scrape(session, url))

                tags = [tag.get('name') for tag in article.get('tags', [])]
                rubrics = [rubric.get('name') for rubric in article.get('rubrics', [])]
                article_metadata.append({
                    'article_id': article.get('id'),
                    'title': article.get('title'),
                    'url': url,
                    'published_dt': published_dt,
                    'tags': tags + rubrics,
                    'meta_description': article.get('meta_description'),
                    'currency_curs': history_curs.get(f"{published_dt}")
                })

        parsed_texts = await asyncio.gather(*parse_tasks, return_exceptions=True)

        for metadata, text in zip(article_metadata, parsed_texts):
            metadata['text'] = text
            result.append(metadata)

    return result


# TODO: Обработка ошибок сервера
async def safe_fetch(session, url, semaphore):
    try:
        async with semaphore:
            await asyncio.sleep(random.uniform(0.5, 1.5))
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"HTTP Error {response.status} for URL: {url}")
                    return None
    except Exception as e:
        # Логирование или обработка исключений
        return None
