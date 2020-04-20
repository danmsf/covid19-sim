from aiohttp import ClientSession
import asyncio
import re
import pandas as pd
from datetime import datetime
from ..settings import  *
import time
import aiohttp
from typing import IO


async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html

async def to_file(url,session,outdir) -> None:

    try:
        html = await fetch_html(url,session)
    except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return url
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return url

    else:
        df = await to_pd(html,url,outdir)
        return df

async def to_pd(html,url,outdir ):
    container = pd.read_html(html, match=READ_HTML_MATCH_PARAM)
    df = container[0]
    df['ref'] = url
    date_str = re.search('\d{8}', url).group()
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    df['date'] = date_obj

    date_repr_to_file = date_obj.strftime('%b-%d-%Y')

    outfile = date_repr_to_file + '.csv'
    outpath = os.path.join(outdir, outfile)
    df.to_csv(outpath)
    return df

async def bulk_crawl_and_write( urls: list, outdir:IO, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    conn = aiohttp.TCPConnector(limit=10)
    async with ClientSession(connector=conn) as session:
        tasks = []
        for i,url in enumerate(urls):
            tasks.append(
                to_file(url=url, session=session,outdir=outdir, **kwargs)
            )
        errors = await asyncio.gather(*tasks)
        return errors

def main(urls,outdir):
    s = time.perf_counter()
    count = 0
    max_count = 3
    all_dfs=[]
    while urls and count < max_count:
        results = asyncio.run(bulk_crawl_and_write(urls=urls, outdir = outdir))
        urls = [element for element in results if hasattr(element,'upper')]
        dfs  = [element for element in results if hasattr(element, 'columns')]
        all_dfs.append(dfs)
        count +=1
        if urls.__len__() > 0:
            logger.info(f'Some errors were met, retrying {count} from {max_count}')

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    return all_dfs

if __name__ == '__main__':
    main()







