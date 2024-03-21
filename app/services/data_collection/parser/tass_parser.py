import asyncio
# import time
# import aiohttp
from datetime import datetime, timedelta

from app.services.async_fetch import safe_fetch
from app.services.async_parser import scrape
# from app.services.yahofin import get_currency_history
from config.settings_parser import MAX_REQUESTS, STEP_HOURS, TIMEOUT, LIMIT_HOST


async def date_generator(start_date, end_date, step_hours=STEP_HOURS):
    current_date = start_date
    while current_date <= end_date:
        yield f"https://tass.ru/tbp/api/v1/search?limit=20&offset=0&lang=ru&types=news&rubrics=mezhdunarodnaya" \
              f"-panorama&rubrics=ekonomika&sort=-es_updated_dt&from_date={current_date.isoformat()}&to" \
              f"_date={(current_date + timedelta(hours=step_hours)).isoformat()}"
        current_date += timedelta(hours=step_hours)


async def get_tass_articles(start, end, session, history_curs):
    # history_curs = get_currency_history(start_date=start, end_date=end)
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    semaphore = asyncio.Semaphore(MAX_REQUESTS)
    urls = [url async for url in date_generator(start_date, end_date)]

    fetch_tasks = [safe_fetch(session, url, semaphore) for url in urls]
    responses = await asyncio.gather(*fetch_tasks, return_exceptions=True)

    parse_tasks = []
    article_metadata = []
    result = []

    for response in responses:
        if response is not None and 'result' in response:
            for article in response.get('result', []):
                url = f"https://tass.ru{article.get('url', '')}"
                published_dt = datetime.fromisoformat(article.get('published_dt')).strftime('%Y-%m-%d')
                parse_tasks.append(scrape(session, url, ['.Paragraph_paragraph__nYCys']))
                tags = [tag.get('name') for tag in article.get('tags', [])]
                rubrics = [rubric.get('name') for rubric in article.get('rubrics', [])]
                article_metadata.append({
                    'article_id': article.get('id'),
                    'title': article.get('title'),
                    'url': url,
                    'published_dt': published_dt,
                    # 'tags': tags + rubrics,
                    # 'meta_description': article.get('meta_description'),
                    'currency_curs': history_curs.get(f"{published_dt}")
                })

    parsed_texts = await asyncio.gather(*parse_tasks, return_exceptions=True)

    for metadata, text in zip(article_metadata, parsed_texts):
        if isinstance(text, dict):
            metadata['text'] = ' '.join(text.get('.Paragraph_paragraph__nYCys'))
        result.append(metadata)

    return result


# async def main():
#     start_time = time.time()
#     async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=LIMIT_HOST),
#                                      timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
#         result = await get_tass_articles('2023-01-01', '2023-06-02', session)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(result)
#     print(f"\n\n Execution Time: {elapsed_time} seconds")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

# 48.047812938690186 seconds - Первый прогон ничего не поменял 1 месяц
# Execution Time: 48.36848783493042 seconds - второй прогон 1 месяц

# Execution Time: 15.576062202453613 seconds без ВПН 1 месяц

# Execution Time: 54.077656507492065 seconds 6 месяцев

