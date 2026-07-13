import logging
import time
import xml.dom.minidom
from concurrent.futures import as_completed
from xml.dom.minidom import Document

import mwparserfromhell
import yaml
from bs4 import BeautifulSoup
from mwparserfromhell.wikicode import Wikicode
from playwright.sync_api import sync_playwright
from requests import Response
from requests.adapters import HTTPAdapter
from requests.exceptions import ChunkedEncodingError
from requests_cache import CachedSession
from requests_futures.sessions import FuturesSession
from urllib3.util import Retry

# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent.
ENDOFLIFE_BOT_USER_AGENT = 'endoflife.date-bot/1.0 (endoflife.date automation; +https://endoflife.date/bot)'
FIREFOX_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'

MAX_RETRIES = 10
BACKOFF_FACTOR = 0.5
MAX_WORKERS = 16
RETRY_STATUS_FORCELIST = [429, 500, 502, 503, 504]

# Created once per process and reused across all fetch_* calls so that:
# - the cache backend (and its on-disk index) is only opened once, instead of on every call;
# - the underlying HTTP connection pool (keep-alive) is shared across calls to the same host.
#
# Respect the caching directives from the server, but provide a fallback expiration time when
# caching directives are not provided. Also use stale responses to avoid errors when the server is down.
_CACHE_SESSION = CachedSession('~/.cache/http', backend='filesystem', cache_control=True, expire_after=86400,
                                stale_if_error=True)
_RETRY = Retry(total=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, status_forcelist=RETRY_STATUS_FORCELIST)
_ADAPTER = HTTPAdapter(pool_connections=MAX_WORKERS, pool_maxsize=MAX_WORKERS, max_retries=_RETRY)
_CACHE_SESSION.mount('http://', _ADAPTER)
_CACHE_SESSION.mount('https://', _ADAPTER)
_FUTURES_SESSION = FuturesSession(session=_CACHE_SESSION, max_workers=MAX_WORKERS)

def fetch_urls(urls: list[str], data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               timeout: int = 30, _remaining_retries: int = MAX_RETRIES) -> list[Response]:
    logging.info(f"Fetching {urls}")

    try:
        session = _FUTURES_SESSION
        headers = {'User-Agent': user_agent}
        start = time.perf_counter()
        futures = [session.get(url, headers=headers, data=data, timeout=timeout, stream=None) for url in urls]
        results = [future.result() for future in as_completed(futures)]
        elapsed = time.perf_counter() - start
        status_codes = [r.status_code for r in results]
        logging.info(f"Fetched {urls}, took {elapsed:.2f}s, status={status_codes}")
        return results
    except ChunkedEncodingError as e:  # See https://github.com/psf/requests/issues/4771#issue-354077499
        next_remaining_retries = _remaining_retries - 1
        if next_remaining_retries == 0:
            logging.error(f"Got ChunkedEncodingError while fetching {urls} ({e}), giving up")
            raise e  # So that the function does not get stuck in an infinite loop.

        # We could wait a bit before retrying, but it's not clear if it would help.
        logging.warning(
            f"Got ChunkedEncodingError while fetching {urls} ({e}), retrying (remaining retries = {next_remaining_retries}).")
        return fetch_urls(urls, data, user_agent, timeout, next_remaining_retries)


def fetch_url(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              timeout: int = 30) -> Response:
    return fetch_urls([url], data, user_agent, timeout)[0]

def fetch_html(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               timeout: int = 30, features: str = "html5lib") -> BeautifulSoup:
    response = fetch_url(url, data, user_agent, timeout)
    return BeautifulSoup(response.text, features=features)

def fetch_json(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              timeout: int = 30) -> dict:
    response = fetch_url(url, data, user_agent, timeout)
    return response.json()

def fetch_yaml(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               timeout: int = 30) -> any:
    response = fetch_url(url, data, user_agent, timeout)
    return yaml.safe_load(response.text)

def fetch_xml(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              timeout: int = 30) -> Document:
    response = fetch_url(url, data, user_agent, timeout)
    return xml.dom.minidom.parseString(response.text)

def fetch_markdown(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              timeout: int = 30) -> Wikicode:
    response = fetch_url(url, data, user_agent, timeout)
    return mwparserfromhell.parse(response.text)

# This requires some setup, see https://playwright.dev/python/docs/intro#installing-playwright.
def fetch_javascript_url(url: str, user_agent: str = ENDOFLIFE_BOT_USER_AGENT, headless: bool = True, wait_until: str = None,
                         wait_for: str = None, select_wait_for: bool = False, click_selector: str = None) -> str:
    logging.info(f"Fetching {url} with JavaScript (wait_until = {wait_until}, wait_for = {wait_for}, select_wait_for = {select_wait_for}, click_selector = {click_selector})")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        context.set_extra_http_headers({'User-Agent': user_agent})

        try:
            page = browser.new_page()
            start = time.perf_counter()
            response = page.goto(url, wait_until=wait_until)
            elapsed = time.perf_counter() - start
            logging.info(f"Fetched {url}, took {elapsed:.2f}s, status={response.status}")

            element_to_wait_for = None
            if wait_for:
                logging.info(f"Waiting for element with selector {wait_for}")
                element_to_wait_for = page.wait_for_selector(selector=wait_for)

            if click_selector:
                logging.info(f"Clicking on element with selector {click_selector}")
                page.click(selector=click_selector)
                page.wait_for_timeout(1000) # Wait for 1 second to allow the page to update after the click.

            return element_to_wait_for.inner_html() if select_wait_for else page.content()
        finally:
            browser.close()
