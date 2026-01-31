# Copilot Instructions for release-data

This repository provides release data for the [endoflife.date](https://endoflife.date) website. Scripts scrape release information from various sources and output structured JSON files.

## Build, Test, and Lint

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Lint code:**
```bash
pre-commit run --all-files
```

**Update all products:**
```bash
python update-release-data.py -v -p '../endoflife.date/products'
```

**Update a single product:**
```bash
python update-release-data.py -v -p '../endoflife.date/products' python
```

**Generate automation report:**
```bash
python report.py -p '../endoflife.date/products'
```

## Architecture

### Data Flow

1. **Product definitions** live in the [endoflife.date repository](https://github.com/endoflife-date/endoflife.date) (`products/*.md` files with YAML frontmatter)
2. **Scraper scripts** (`src/*.py`) fetch release data from various sources (Git tags, GitHub releases, APIs, HTML scraping)
3. **Output** goes to `releases/*.json` files with versioned release dates
4. **GitHub Actions** runs updates 4x daily and commits changes automatically

### Core Components

**`src/common/`** - Shared utilities:
- `endoflife.py`: Parses product frontmatter, handles `auto` config (regex patterns, version templates)
- `releasedata.py`: Manages `releases/*.json` files via `ProductData` context manager
- `dates.py`: Date/time utilities
- `git.py`, `github.py`, `http.py`: Source-specific helpers

**Scraper scripts** (`src/*.py`):
- Each script is standalone and rebuilds data from scratch (never relies on existing JSON)
- Uses `ProductData` context manager that auto-saves on success or raises `ProductUpdateError` on failure
- Filters versions via `config.first_match(version_str)` and renders via `config.render(match)`

**Main orchestrator** (`update-release-data.py`):
- Reads product frontmatter from website repo
- Executes relevant scripts for each product
- Tracks execution times and failures
- Outputs GitHub Actions summary

## Key Conventions

### Product Frontmatter Auto Config

Products define automation in YAML frontmatter:
```yaml
auto:
  methods:
    - git: https://github.com/example/repo
      regex: '^v?(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.(?P<patch>[0-9]+)$'
      template: '{{major}}.{{minor}}.{{patch}}'
```

- **method**: Determines which `src/{method}.py` script runs
- **regex**: Filters version strings (can be list for multiple patterns)
- **regex_exclude**: Excludes matched versions
- **template**: Liquid template to render version names from regex groups

### Script Patterns

All scripts follow this structure:
```python
from common.releasedata import ProductData, config_from_argv

config = config_from_argv()
with ProductData(config.product) as product_data:
    for version_str in fetch_versions_from_source():
        match = config.first_match(version_str)
        if match:
            version = config.render(match)
            product_data.declare_version(version, release_date)
```

The `ProductData` context manager:
- Automatically loads existing data on `__enter__`
- Validates updates occurred (raises error if `updated=False`)
- Saves sorted JSON on `__exit__`
- Handles errors by reverting changes

### Version Handling

- **Stable only**: No beta, RC, nightly versions
- **Dates**: YYYY-MM-DD format, preferably in release's timezone
- **Sorting**: Versions sorted by (date, name) descending; releases sorted by name descending
- **Identifiers**: Use `endoflife.to_identifier()` for consistent naming

### JSON Output Format

```json
{
  "releases": {
    "1.2": {
      "name": "1.2",
      "releaseDate": "2024-01-15",
      "releaseLabel": "optional-label",
      "eol": "2025-01-15",
      "eoas": "2024-07-15",
      "eoes": "2024-10-15"
    }
  },
  "versions": {
    "1.2.3": {
      "name": "1.2.3",
      "date": "2024-01-15"
    }
  }
}
```

- **releases**: Lifecycle data (EOL dates) - coarser-grained
- **versions**: Point release dates - finer-grained

### Cumulative Updates

If `auto.cumulative: true` in frontmatter:
- Script should **not** delete existing data before running
- New data is merged with existing data
- Used when multiple scripts contribute to the same product

### Guiding Principles

1. Scripts must be standalone and simple
2. Never rely on existing data - rebuild from scratch each run
3. Code should handle upstream changes gracefully
4. Everything runs on GitHub Actions (no local state dependencies)
