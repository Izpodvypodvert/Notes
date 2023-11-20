import aiohttp


async def fetch_activity(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            return response_json
