import re
from datetime import datetime
from bs4 import BeautifulSoup
from common import dates, endoflife, http, releasedata

# This script fetches the Sourcegraph technical changelog and releases pages,
# extracts relevant version and release date information, and declares them using ProductData.
# The version number is extracted from the technical changelog and then matched correctly with the release date from the release pages.
# The Version number is from the h2 tag. Each h2 has a matching h1 tag (eg 5.11 patch 4) which then matches with the 5.11 patch 4 on the release pages
# Sourcegraph does not specify the day of release for each version. This has been defaulted to the 1st of every month for now


URLS = [
    "https://sourcegraph.com/docs/technical-changelog",
    "https://sourcegraph.com/docs/releases"
]

# Function to convert date to YYYY-MM-DD format
def convert_date(date_str):
    try:
        date = datetime.strptime(date_str, '%B %Y')
        return date.strftime('%Y-%m-%d')
    except ValueError:
        return date_str  # Return original if parsing fails

with releasedata.ProductData("sourcegraph") as product_data:
    responses = http.fetch_urls(URLS)
    
    heading_pairs = []
    release_data = []

    # Process each response
    for response in responses:
        soup = BeautifulSoup(response.text, 'html5lib')

        if "technical-changelog" in response.url:
            # Extract h1 and h2 elements with their texts
            current_h1 = None
            pattern = re.compile(r'^v\d+(\.\d+)*')
            for tag in soup.find_all(['h1', 'h2']):
                text = tag.get_text().strip()
                if tag.name == 'h1':
                    current_h1 = text
                elif tag.name == 'h2' and current_h1 and pattern.match(text):
                    clean_text = text.lstrip('v')  # Remove leading 'v'
                    heading_pairs.append((current_h1, clean_text))

        elif "releases" in response.url:
            # Extract the table rows
            table = soup.find('table')
            rows = table.find_all('tr')[1:]  # Skip the header row

            for row in rows:
                cols = row.find_all('td')
                release = cols[0].get_text().strip()
                date = convert_date(cols[1].get_text().strip())
                release_data.append((release, date))

    # Match h1 and h2 elements with release data
    matching_data = []
    for h1, h2 in heading_pairs:
        for release, date in release_data:
            if h1.lower() in release.lower():
                matching_data.append((h2, date))

    # Print the matched data and declare versions
    for h2, date in matching_data:
        print(f"h2: {h2} - Date: {date}")

        parsed_date = dates.parse_date(date, formats=["%Y-%m-%d"])
        if parsed_date and h2 and endoflife.DEFAULT_VERSION_PATTERN.match(h2):
            product_data.declare_version(h2, parsed_date)
            print(f"Declared version {h2} with date {parsed_date}")
