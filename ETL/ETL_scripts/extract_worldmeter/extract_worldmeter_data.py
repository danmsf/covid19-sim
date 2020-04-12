from ETL_scripts.extract_worldmeter.utils.functions import *
from ETL_scripts.extract_worldmeter.utils.nonsync import main as download_async
from selenium import webdriver

def main(outdir:IO)->None:
    # Validate
    handle_first_time()

    # create a new instance of Chrome
    logger.info('>>Opening chromium in background')
    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

    # send a get request to the appropiate webpage
    # (in this case the download_dfs archive page from "The Wayback Machine" for "https://www.worldometers.info/coronavirus/")
    logger.info(f'>>Connecting to URL..waiting for response')
    browser.get(WAYBACK_FULLPATH)

    # Handle a timeout
    timeout_get_request(browser, 50)

    # Get only new raw_data
    logger.info('>>Checking for new links in URL')
    prev_urls = get_prev_urls(outdir)
    all_urls = get_all_urls_matching_regex(browser, URL_REGEX_PATTERN)
    new_urls = get_fresh_urls(all_urls, prev_urls, excluded_urls)

    # Iterate over hrefs and download tables from site
    if new_urls:
        logger.info(f'>>Downloading data from links: {len(new_urls)} files')
        dfs = download_async(new_urls,outdir)
    else:
        logger.info('>>No new links')


    logger.info('>>Quitting chromium')
    logger.info('>>End program')
    browser.quit()

if __name__ == '__main__':
    main()
