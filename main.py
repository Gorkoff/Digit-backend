import asyncio

import uvicorn

from app.api import app


async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    task_api = asyncio.create_task(start_api())
    await asyncio.gather(task_api)


if __name__ == '__main__':
    asyncio.run(main())