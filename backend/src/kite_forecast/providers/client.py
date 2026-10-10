import logging

import httpx

logger = logging.getLogger(__name__)


async def get_json(url: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)

        if response.status_code == 429:
            logger.warning(
                "Open-Meteo rate limit: status=%s, body=%s",
                response.status_code,
                response.text,
            )

        response.raise_for_status()
        return response.json()
