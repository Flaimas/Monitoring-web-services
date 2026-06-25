from handlers.handlers import handle_add_response, handle_url_output
import httpx
from httpx import AsyncClient
import time
import asyncio

async def check_url(client: AsyncClient, host: str) -> tuple[int, float]:
    try:
        url = "https://" + host
        start = time.perf_counter()
        response = await client.get(url=url)
        end = time.perf_counter()
        duration = round(end - start, 3)
        return response.status_code, duration
    except Exception as e:
        return 500, 0.0

async def run_monitoring_loop(timeout: int = 5):
    async with httpx.AsyncClient(timeout=timeout) as client:
        while True:
            hosts = await handle_url_output(only_active=True)
            tasks = [check_url(client, site.url) for site in hosts]
            result = await asyncio.gather(*tasks)
            for site, res in zip(hosts, result):
                status_code, response_time = res
                await handle_add_response(service_id=site.id, status_code=status_code, response_time=response_time)
            await asyncio.sleep(10)