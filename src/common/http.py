import logging
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
FIREFOX_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0'

def fetch_urls(urls: list[str], data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> list[Response]:
    logging.info(f"Fetching {urls}")

    try:
        # Respect the caching directives from the server,
        # but provides a fallback expiration time when caching directives are not provided.
        # Also use stale responses to avoid errors when the server is down.
        cache_session = CachedSession('~/.cache/http', backend='filesystem', cache_control=True, expire_after=86400, stale_if_error=True)
        with FuturesSession(session=cache_session) as session:
            adapter = HTTPAdapter(max_retries=Retry(total=max_retries, backoff_factor=backoff_factor))
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            headers = {'User-Agent': user_agent}
            futures = [session.get(url, headers=headers, data=data, timeout=timeout, stream=None) for url in urls]
            results = [future.result() for future in as_completed(futures)]

            logging.info(f"Fetched {urls}")
            return results
    except ChunkedEncodingError as e:  # See https://github.com/psf/requests/issues/4771#issue-354077499
        next_max_retries = max_retries - 1
        if next_max_retries == 0:
            logging.error(f"Got ChunkedEncodingError while fetching {urls} ({e}), giving up")
            raise e  # So that the function does not get stuck in an infinite loop.

        # We could wait a bit before retrying, but it's not clear if it would help.
        logging.warning(
            f"Got ChunkedEncodingError while fetching {urls} ({e}), retrying (remaining retries = {next_max_retries}).")
        return fetch_urls(urls, data, user_agent, next_max_retries, backoff_factor, timeout)


def fetch_url(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> Response:
    return fetch_urls([url], data, user_agent, max_retries, backoff_factor, timeout)[0]

def fetch_html(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30,
               features: str = "html5lib") -> BeautifulSoup:
    response = fetch_url(url, data, user_agent, max_retries, backoff_factor, timeout)
    return BeautifulSoup(response.text, features=features)

def fetch_json(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> Document:
    response = fetch_url(url, data, user_agent, max_retries, backoff_factor, timeout)
    return response.json()

def fetch_yaml(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
               max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> any:
    response = fetch_url(url, data, user_agent, max_retries, backoff_factor, timeout)
    return yaml.safe_load(response.text)

def fetch_xml(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> Document:
    response = fetch_url(url, data, user_agent, max_retries, backoff_factor, timeout)
    return xml.dom.minidom.parseString(response.text)

def fetch_markdown(url: str, data: any = None, user_agent: str = ENDOFLIFE_BOT_USER_AGENT,
              max_retries: int = 10, backoff_factor: float = 0.5, timeout: int = 30) -> Wikicode:
    response = fetch_url(url, data, user_agent, max_retries, backoff_factor, timeout)
    return mwparserfromhell.parse(response.text)

# This requires some setup, see https://playwright.dev/python/docs/intro#installing-playwright.
def fetch_javascript_url(url: str, user_agent: str = ENDOFLIFE_BOT_USER_AGENT, wait_until: str = None, wait_for: str = None, select_wait_for: bool = False) -> str:
    logging.info(f"Fetching {url} with JavaScript (wait_until = {wait_until}, wait_for = {wait_for}, select_wait_for = {select_wait_for})")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        context.set_extra_http_headers({'User-Agent': user_agent})

        try:
            page = browser.new_page()
            page.goto(url, wait_until=wait_until)
            logging.info(f"Fetched {url}")

            if wait_for:
                try:
                    logging.info(f"Waiting for element with selector {wait_for}")
                    element = page.wait_for_selector(selector=wait_for)

                    if element:
                        logging.debug(f"Found element with selector {wait_for} on {url}")
                        return element.inner_html() if select_wait_for else page.content()

                    logging.error(f"No element found with selector {wait_for} on {url}, will return full page content")
                    logging.debug(f"Full page content: {page.content()}")

                except Exception as e:  # noqa: BLE001
                    logging.error(f"Error while waiting for element with selector {wait_for} on {url}: {e}")
                    logging.debug(f"Full page content: {page.content()}")

            return page.content()
        finally:
            browser.close()
