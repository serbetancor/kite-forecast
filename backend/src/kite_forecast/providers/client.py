import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = httpx.Timeout(
    connect=30.0,
    read=30.0,
    write=10.0,
    pool=10.0,
)

MAX_ATTEMPTS = 4
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


async def get_json(url: str) -> dict[str, object]:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                response = await client.get(url)

                if response.status_code == 429:
                    logger.warning(
                        "Open-Meteo rate limit: status=%s, body=%s",
                        response.status_code,
                        response.text,
                    )

                response.raise_for_status()
                return response.json()

            except (httpx.TimeoutException, httpx.ConnectError):
                if attempt == MAX_ATTEMPTS:
                    raise

                logger.warning(
                    "Open-Meteo connection failed. " "Retrying (attempt %s/%s)",
                    attempt,
                    MAX_ATTEMPTS,
                )

            except httpx.HTTPStatusError as error:
                status_code = error.response.status_code

                if status_code not in RETRYABLE_STATUS_CODES or attempt == MAX_ATTEMPTS:
                    raise

                logger.warning(
                    "Open-Meteo returned HTTP %s. " "Retrying (attempt %s/%s)",
                    status_code,
                    attempt,
                    MAX_ATTEMPTS,
                )

            await asyncio.sleep(2**attempt)

    raise RuntimeError("Open-Meteo request failed unexpectedly")
