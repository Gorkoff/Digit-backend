import asyncio
import time
from datetime import datetime

import aiohttp

from app.services.async_fetch import safe_fetch
from app.services.async_parser import scrape
from config.settings_parser import MAX_REQUESTS, LIMIT_HOST, TIMEOUT
from app.services.yahofin import get_currency_history


async def get_rbk_articles(start_date, end_date, session):
    current_page = 0
    start = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    end = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    semaphore = asyncio.Semaphore(MAX_REQUESTS)
    history_curs = get_currency_history(start_date=start_date, end_date=end_date)
    result = []
    while True:
        url = f"https://www.rbc.ru/search/ajax/?query=&project=rbcnews&category=finances%2Ceconomics%2Cbusiness&types" \
              f"=short_news&dateFrom={start}&dateTo={end}&page={current_page}"
        fetch_task = safe_fetch(session, url, semaphore)
        responses = await asyncio.gather(fetch_task, return_exceptions=True)
        if responses[0].get('items') != []:
            parse_tasks = []
            article_metadata = []
            for article in responses[0].get('items'):
                published_dt = datetime.utcfromtimestamp(article.get('publish_date_t')).strftime('%Y-%m-%d')
                parse_tasks.append(
                    scrape(session, article.get('fronturl'), ['.article__text_free', '.article__tags__item']))
                article_metadata.append({
                    'article_id': article.get('id'),
                    'title': article.get('title'),
                    'url': article.get('fronturl'),
                    'published_dt': published_dt,
                    'meta_description': article.get('title'),
                    'currency_curs': history_curs.get(f"{published_dt}")
                })
            parsed_texts = await asyncio.gather(*parse_tasks, return_exceptions=True)
            for metadata, text in zip(article_metadata, parsed_texts):
                metadata['text'] = ' '.join(text.get('.article__text_free'))
                metadata['tags'] = text.get('.article__tags__item')
                result.append(metadata)
        else:
            break
        current_page += 1
    return result


async def main():
    start_time = time.time()
    connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        result = await get_rbk_articles('2023-08-01', '2023-08-30', session)
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Execution Time: {elapsed_time} seconds")

# Execution Time: 18.61995005607605 seconds
# Execution Time: 18.20568060874939 seconds

if __name__ == "__main__":
    asyncio.run(main())
