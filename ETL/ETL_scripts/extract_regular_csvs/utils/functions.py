from aiohttp import ClientSession
import asyncio
import pandas as pd
from io import StringIO
import aiohttp


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def to_file(url,session) -> None:

    html = await fetch_html(url,session)
    df = await to_pd(html)
    return df

async def to_pd(html):
    df = pd.read_csv(StringIO(html))
    return df

async def bulk_crawl_and_write( urls: list, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    conn = aiohttp.TCPConnector(limit=10)
    async with ClientSession(connector=conn) as session:
        tasks = []
        for url in urls:
            tasks.append(
                to_file(url=url, session=session, **kwargs)
            )
        errors = await asyncio.gather(*tasks)
        return errors

def download_dfs(urls):
    results = asyncio.run(bulk_crawl_and_write(urls=urls))
    dfs  = [element for element in results if hasattr(element, 'columns')]
    return dfs









