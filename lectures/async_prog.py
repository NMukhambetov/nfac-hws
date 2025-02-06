import asyncio

import aiohttp


async def get_google():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://0.0.0.0:8080') as response:
            response_json = await response.json()
            for movie in response_json.get('movies', []):
                print(f"Title: {movie['title']}, Rating: {movie['rating']}")


asyncio.run(get_google())