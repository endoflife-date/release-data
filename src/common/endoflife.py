import json
import frontmatter
from concurrent.futures import as_completed
from glob import glob
from os import path
from requests import Response
from requests.adapters import HTTPAdapter
from requests.exceptions import ChunkedEncodingError
from requests_futures.sessions import FuturesSession
from urllib3.util import Retry

# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'


def load_product(product_name, pathname="website/products") -> frontmatter.Post:
    """Load the product's file frontmatter.
    """
    with open(f"{pathname}/{product_name}.md", "r") as f:
        return frontmatter.load(f)


def list_products(method, products_filter=None, pathname="website/products") -> dict[str, list[dict]]:
    """Return a list of products that are using the same given update method.
    """
    products_with_method = {}

    for product_file in glob(f"{pathname}/*.md"):
        product_name = path.splitext(path.basename(product_file))[0]
        if products_filter and product_name != products_filter:
            continue

        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            if "auto" in data:
                configs = list(filter(
                    lambda config: method in config.keys(),
                    data["auto"]
                ))
                if len(configs) > 0:
                    products_with_method[product_name] = configs

    return products_with_method


# Keep the default timeout high enough to avoid errors with web.archive.org.
def fetch_urls(urls, data=None, headers=None, max_retries=10, backoff_factor=0.5, timeout=30) -> list[Response]:
    try:
        with FuturesSession() as session:
            adapter = HTTPAdapter(max_retries=Retry(total=max_retries, backoff_factor=backoff_factor))
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            headers = {'User-Agent': USER_AGENT} | ({} if headers is None else headers)
            futures = [session.get(url, headers=headers, data=data, timeout=timeout, stream=None) for url in urls]
            return [future.result() for future in as_completed(futures)]
    except ChunkedEncodingError as e:  # See https://github.com/psf/requests/issues/4771#issue-354077499
        next_max_retries = max_retries - 1
        if next_max_retries == 0:
            raise e  # So that the function does not get stuck in an infinite loop.
        else:
            # We could wait a bit before retrying, but it's not clear if it would help.
            print(f"Got ChunkedEncodingError while fetching {urls} ({e}), retrying (remaining retries = {next_max_retries}).")
            return fetch_urls(urls, data, headers, next_max_retries, backoff_factor, timeout)


def fetch_url(url, data=None, headers=None, max_retries=5, backoff_factor=0.5, timeout=30) -> str:
    return fetch_urls([url], data, headers, max_retries, backoff_factor, timeout)[0].text


def write_releases(product, releases, pathname="releases") -> None:
    with open(f"{pathname}/{product}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))
