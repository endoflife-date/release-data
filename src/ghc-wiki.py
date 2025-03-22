"""
In addition to automation from git tags,
use the GHC-status wiki page on GHC gitlab
as a source for "Not recommended for use" end-of-support signals.

References:
    https://github.com/endoflife-date/release-data/pull/395
    https://github.com/endoflife-date/endoflife.date/pull/6287
    https://gitlab.haskell.org/ghc/ghc/-/wikis/GHC-status
"""

import logging
import re
import sys

from common import dates, endoflife, http, releasedata

def parse_markdown_tables(lineiter):
    """ Generator. Yields found tables until StopIteration """
    while True:
        try:
            #-- fast-forward to table header
            while True:
                line = next(lineiter)
                header = maybe_markdown_table_row(line)
                if header:
                    break
            #-- underline
            hr = maybe_markdown_table_row(next(lineiter))
            assert len(hr) == len(header)
            assert all(set(x) == {'-'} for x in hr)
            #-- rows
            rows = []
            while True:
                line = next(lineiter)
                cells = maybe_markdown_table_row(line)
                if not cells:
                    break
                assert len(cells) == len(header)
                rows.append(cells)
            yield [header] + rows
        except StopIteration:
            return # f**ing PEP 479

def maybe_markdown_table_row(line):
    line = line.strip()
    if not re.match(r'[|].*[|]', line):
        return None
    return [x.strip() for x in line.strip('|').split('|')]

def main():
    with releasedata.ProductData("ghc") as product:
        resp = http.fetch_url("https://gitlab.haskell.org/api/v4/projects/1/wikis/GHC-Status")
        resp.raise_for_status()
        data = resp.json()
        assert data['title'] == "GHC Status"
        assert data['format'] == "markdown"
        md = data['content'].splitlines()

        #-- Parse tables out of the wiki text. At time of writing, the script expects exactly two:
        #-- 1. "Most recent major" with 5 columns
        #-- 2. "All released versions" with 5 columns
        [series_table, patchlevel] = parse_markdown_tables(iter(md))

        for row in series_table[1:]:
            [series, _downloadlink, mostrecent, nextplanned, status] = row
            series = series.split(' ') [0]
            series = series.replace('\\.', '.')
            if series == "Nightlies": continue
            mostrecent = mostrecent.lstrip('%').replace('"', '')
            status = status.lower()

            #-- See discussion in https://github.com/endoflife-date/endoflife.date/pull/6287
            r = product.get_release(series)
            #-- The clearest semblance of an EOL signal we get
            r.set_eol("not recommended for use" in status or ":red_circle:" in status)
            #-- eoasColumn label is "Further releases planned"
            r.set_eoas(any(keyword in nextplanned for keyword in ("None",  "N/A")))
            #-- Initial release in major series is x.y.1
            r.set_field('latest', mostrecent)
            if not mostrecent.endswith('.1'):
                latest = product.get_version(mostrecent)
                if latest:
                    r.set_field('latestReleaseDate', latest.date())

        for row in patchlevel[1:]:
            [milestone, _downloadlink, date, _ticket, _manager] = row
            version = milestone.lstrip('%')
            version = version.split(' ') [0]
            date = dates.parse_date(date)
            product.declare_version(version, date)


# TODO at some point maybe use https://gitlab.haskell.org/ghc/release/release-metadata/

try:
    main()
except AssertionError:
    logging.exception("When parsing wiki tables")
    sys.exit(1)
except:
    logging.exception("Failed to refresh product data")
    sys.exit(1)
