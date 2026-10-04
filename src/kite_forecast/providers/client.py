import httpx


async def get_json(url: str) -> dict[str, object]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
