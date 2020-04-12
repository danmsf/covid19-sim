from aiohttp import ClientSession
import asyncio
import pandas as pd
from io import StringIO
import aiohttp

class Entry(object):
    def __init__(self,url=None , name = None, df= None, *args):
        self.url = url
        self.name = name
        self.df = df

class Entries(object):
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

def df_to_entries(df):
    entries = []
    for _, rows in df.iterrows():
        entry = Entry(rows.url, rows.urlname)
        entries.append(entry)
    return entries


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def to_file(entry,session) -> None:

    html = await fetch_html(entry.url,session)
    df = await to_pd(html)
    entry.df = df
    return entry

async def to_pd(html):
    df = pd.read_csv(StringIO(html))
    return df

async def bulk_crawl_and_write( entries: list, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    conn = aiohttp.TCPConnector(limit=10)
    async with ClientSession(connector=conn) as session:
        tasks = []
        for entry in entries:
            tasks.append(
                to_file(entry=entry, session=session, **kwargs)
            )
        errors = await asyncio.gather(*tasks)
        return errors

def download_dfs(entries):
    results = asyncio.run(bulk_crawl_and_write(entries=entries))
    return results






