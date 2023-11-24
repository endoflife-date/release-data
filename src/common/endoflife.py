import json
import frontmatter
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from glob import glob
from os import path

# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'


def load_product(product_name, pathname="website/products"):
    """Load the product's file frontmatter.
    """
    with open(f"{pathname}/{product_name}.md", "r") as f:
        return frontmatter.load(f)


def list_products(method, products_filter=None, pathname="website/products"):
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
def fetch_url(url, retry_count=5, timeout=30, data=None, headers=None):
    headers = {'User-Agent': USER_AGENT} | {} if headers is None else headers
    with Session() as s:
        s.mount('https://', HTTPAdapter(max_retries=Retry(total=retry_count, backoff_factor=0.2)))
        r = s.get(url, headers=headers, data=data, timeout=timeout)
        return r.text


def write_releases(product, releases, pathname="releases"):
    with open(f"{pathname}/{product}.json", "w") as f:
        f.write(json.dumps(dict(
            # sort by date then version (desc)
            sorted(releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
        ), indent=2))
