import asyncio
from handlers.handler_tass import get_responce

start = '2023-10-01'
end = '2023-10-1'


async def main():
    task_get_articles = asyncio.create_task(get_responce(start, end))
    await asyncio.gather(task_get_articles)


if __name__ == '__main__':
    asyncio.run(main())
