## Setting up a development environment

The scripts in this project require the Python version specified in [`.python-version`](.python-version).

1. Clone this repository:

   ```shell
   git clone https://github.com/endoflife-date/release-data.git
   cd release-data
   ```

2. Create and activate a virtual environment in `.venv`:

   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   All commands in this guide assume this virtual environment is activated, i.e. that you have run
   `source .venv/bin/activate` in your current shell. You will need to re-run this command in every
   new shell session.

3. Install the Python dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Install the [pre-commit](https://pre-commit.com/) hooks, which run [ruff](https://docs.astral.sh/ruff/)
   and a few other sanity checks (see [`.pre-commit-config.yaml`](.pre-commit-config.yaml)) before every commit:

   ```shell
   pre-commit install
   ```

5. Both scripts described below operate on the release data in this repository (`releases/`)
   together with the product definitions (`products/*.md`) from the [endoflife.date](https://github.com/endoflife-date/endoflife.date) repository.
   You will therefore need a local clone of that repository as well, for example as a sibling directory:

   ```shell
   git clone https://github.com/endoflife-date/endoflife.date.git ../endoflife.date
   ```

## Running `update-release-data.py`

`update-release-data.py` runs the individual "auto update" scripts declared in each product's frontmatter (those listed in the `auto` key),
to fetch the latest release information for each product, and stores the results as JSON files under `releases/`.

```shell
python update-release-data.py --product-dir ../endoflife.date/products
```

To restrict the update to a single product, pass the product name as a positional argument:

```shell
python update-release-data.py --product-dir ../endoflife.date/products docker-engine
```

Run `python update-release-data.py -h` for the full list of options.

## Running `update-product-data.py`

`update-product-data.py` reads the JSON release data produced by `update-release-data.py` (under `releases/`)
and uses it to update the `releases` in the corresponding product Markdown files of the `endoflife.date` repository.

```shell
python update-product-data.py --product-dir ../endoflife.date/products
```

To restrict the update to a single product, pass the product name as a positional argument:

```shell
python update-product-data.py --product-dir ../endoflife.date/products docker-engine
```

Run `python update-product-data.py -h` for the full list of options.

## Adding a new auto-update method

If you want to add a new auto-update method, create a new script under [`src/`](src/) with the name `<method_name>.py`.

For example, a minimal script looks like:

```python
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    for version_str, release_date in fetch_versions_from_source(config.url):
        match = config.first_match(version_str)
        if match:
            version = config.render(match)
            product_data.declare_version(version, release_date)
```

Once created, the script is used by referencing its name as a key under a product's `auto.methods`
frontmatter entry (in the [`endoflife.date`](https://github.com/endoflife-date/endoflife.date) repository), for example:

```yaml
auto:
  methods:
    - my_method: https://example.com/releases
      regex: '^v?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$'
```

All new scripts must adhere to the following guiding principles:

* Reuse the existing infrastructure code in [`src/common/`](src/common/) (e.g. `http.py` for HTTP requests with caching/retries, `github.py` for the GitHub API, `dates.py` for date parsing).
* Do not rely on existing data: rebuild the product's release data from scratch on every run.
* Be runnable unattended on GitHub Actions (no local state or interactive steps).

Do not hesitate to take a look at existing scripts for inspiration, for example
[`github_releases.py`](src/github_releases.py), [`npm.py`](src/npm.py), or [`php.py`](src/php.py).

## Code style

This repository uses [ruff](https://docs.astral.sh/ruff/) for linting, configured in [`.ruff.toml`](.ruff.toml).
Linting runs automatically via pre-commit and in CI. You can run it manually with:

```shell
pre-commit run --all-files
```
