import argparse
import time
from pathlib import Path

from src.common import endoflife

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create report on product automation.')
    parser.add_argument('-p', '--product-dir', required=True, help='path to the product directory')
    args = parser.parse_args()

    products_dir = Path(args.product_dir)
    products = endoflife.list_products(products_dir)
    count_auto = len([product for product in products if product.auto_configs()])

    print(f"As of {time.strftime('%Y-%m-%d')}, {count_auto} of the {len(products)} products"
          f" tracked by endoflife.date have automatically tracked releases:")
    print()
    print('| Product | Permalink | Auto | Method(s) |')
    print('|---------|-----------|------|-----------|')
    for product in products:
        title = product.get_title()
        permalink = product.get_permalink()
        auto = '✔️' if product.has_auto_configs() else '❌'
        methods = ', '.join(sorted({config.method for config in product.auto_configs()}))
        print(f"| {title} | [`{permalink}`](https://endoflife.date{permalink}) | {auto} | {methods} |")
    print()
    print('This table has been generated by [report.py](/report.py).')
