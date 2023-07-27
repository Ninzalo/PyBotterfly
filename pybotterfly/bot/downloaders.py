import asyncio
import aiohttp


async def download_file(
    url: str, _session: aiohttp.ClientSession | None = None
) -> bytes:
    if _session != None:
        session = _session
    else:
        session = aiohttp.ClientSession()
    async with session:
        async with asyncio.BoundedSemaphore(5):
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()
                else:
                    await asyncio.sleep(1)
                    return await download_file(url=url, _session=session)
