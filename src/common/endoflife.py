import frontmatter
import urllib.request

from glob import glob
from os import path

# See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent.
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'


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


def fetch_url(url, retry_count=2, timeout=5, data=None, headers=None, encoding='utf-8'):
    last_exception = None

    headers = {'User-Agent': USER_AGENT} | {} if headers is None else headers
    request = urllib.request.Request(url, headers=headers)

    for retry in range(0, retry_count):
        try:
            resp = urllib.request.urlopen(request, data=data, timeout=timeout)
            return resp.read().decode(encoding)
        except Exception as e:
            last_exception = e
            print(f"Fetch of {url} failed (retry={retry}), got: " + str(e))
            continue

    raise last_exception
