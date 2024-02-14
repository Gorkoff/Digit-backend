import asyncio
import random


async def safe_fetch(session, url, semaphore):
    try:
        async with semaphore:
            # await asyncio.sleep(random.uniform(0.5, 1.5))
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"HTTP Error {response.status} for URL: {url}")
                    return None
    except Exception as e:
        # Логирование или обработка исключений
        return None
