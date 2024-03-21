async def safe_fetch(session, url, semaphore):
    try:
        async with semaphore:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"HTTP Error {response.status} for URL: {url}")
                    return None
    except Exception as e:
        # TODO: Логирование или обработка исключений нужно добавить
        return None
