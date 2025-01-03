import logging
import re

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
        #-- parse tables, here we expect three
        [series_table, patchlevel9x, patchlevel8x] = parse_markdown_tables(iter(md))

        for row in patchlevel9x[1:]:
            [milestone, date, _ticket, _manager, _download] = row
            version = milestone.lstrip('%')
            date = (date # kludges for inconsistencies in handwritten dates
                .replace("Sept", "Sep")
                #.replace("November", "Nov")
                #.replace("April", "Apr")
                #.replace("July", "Jul")
            )
            date = dates.parse_date(date, ['%d %b %Y', '%d %B %Y'])
            product.declare_version(version, date)

        # NOTE: versions in patchlevel8x ignored by the script, all EOL at this point.

        for row in series_table[1:]:
            [series, mostrecent, nextplanned, status] = row
            series = series.replace('\\.', '.')
            if series == "Nightlies": continue
            mostrecent = mostrecent.lstrip('%').replace('"', '')
            status = status.lower()

            #-- See discussion in https://github.com/endoflife-date/endoflife.date/pull/6287
            r = product.get_release(series)
            #-- The clearest semblance of an EOL signal we get
            r.set_eol("not recommended for use" in status or ":red_circle:" in status)
            #-- eoasColumn label is "Further releases planned"
            r.set_eoas(nextplanned in ("None", "N/A", ""))
            #-- Initial release in major series is x.y.1
            r.set_field('latest', mostrecent)
            if not mostrecent.endswith('.1'):
                latest = product.get_version(mostrecent)
                if latest:
                    r.set_field('latestReleaseDate', latest.date())

# TODO also https://gitlab.haskell.org/ghc/release/release-metadata/

try:
    main()
except AssertionError:
    logging.exception("When parsing wiki tables")
except:
    logging.exception("Failed to refresh product data")
