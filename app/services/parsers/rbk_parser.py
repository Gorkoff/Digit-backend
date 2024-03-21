import asyncio
# import time
from datetime import datetime

# import aiohttp

from app.services.async_fetch import safe_fetch
from app.services.async_parser import scrape
from config.settings_parser import MAX_REQUESTS, LIMIT_HOST, TIMEOUT
# from app.services.parsers.yahofin import get_currency_history


async def fetch_and_parse(session, url, semaphore, history_curs):
    fetch_task = safe_fetch(session, url, semaphore)
    response = await fetch_task
    if response.get('items'):
        parse_tasks = []
        article_metadata = []
        for article in response.get('items'):
            published_dt = datetime.utcfromtimestamp(article.get('publish_date_t')).strftime('%Y-%m-%d')
            parse_tasks.append(
                scrape(session, article.get('fronturl'), ['.article__text_free']))
            article_metadata.append({
                'article_id': article.get('id'),
                'title': article.get('title'),
                'url': article.get('fronturl'),
                'published_dt': published_dt,
                # 'meta_description': article.get('title'),
                'currency_curs': history_curs.get(published_dt)
            })
        parsed_texts = await asyncio.gather(*parse_tasks, return_exceptions=True)
        for metadata, text in zip(article_metadata, parsed_texts):
            if isinstance(text, dict):
                metadata['text'] = ' '.join(text.get('.article__text_free'))
                # metadata['tags'] = text.get('.article__tags__item')
        return article_metadata
    return []


async def get_rbk_articles(start_date, end_date, session, history_curs):
    start = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    end = datetime.strptime(end_date, "%Y-%m-%d").strftime("%d.%m.%Y")

    # history_curs = get_currency_history(start_date=start_date, end_date=end_date)
    semaphore = asyncio.Semaphore(MAX_REQUESTS)
    result = []

    current_page = 0
    while True:
        url = f"https://www.rbc.ru/search/ajax/?query=&project=rbcnews&category=finances%2Ceconomics%2Cbusiness&types" \
              f"=short_news&dateFrom={start}&dateTo={end}&page={current_page}"

        article_metadata = await fetch_and_parse(session, url, semaphore, history_curs)
        if not article_metadata:
            break
        result.extend(article_metadata)
        current_page += 1
    return result


# async def main():
#     start_time = time.time()
#     connector = aiohttp.TCPConnector(limit_per_host=LIMIT_HOST)
#     timeout = aiohttp.ClientTimeout(total=TIMEOUT)
#     async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
#         result = await get_rbk_articles('2023-01-01', '2023-06-02', session)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(result)
#     print(f"\n\n Execution Time: {elapsed_time} seconds")

 # Execution Time: 18.59790539741516 seconds 1 месяц
 # Execution Time: 17.309295415878296 seconds 1 месяц

#  Execution Time: 19.23914408683777 seconds 6 месяцев

# Execution Time: 21.520447969436646 seconds

# if __name__ == "__main__":
#     asyncio.run(main())
