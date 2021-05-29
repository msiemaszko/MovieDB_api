import httpx
import asyncio
import json
from src.consts import *


async def request(client, imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = await client.get(url)
    return json.loads(response.text)


async def load_data_from_omdb(id_list: list):
    async with httpx.AsyncClient() as client:
        tasks = [request(client, imdb_id) for imdb_id in id_list]
        result = await asyncio.gather(*tasks)
        return result
