import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# utility fnctions
def extract_version_and_date(input_string):
    # Extract version number using regular expression
    version_match = re.search(r'Chrome (\d+):', input_string)
    if version_match:
        version = version_match.group(1)
    else:
        version = None

    # Extract date using datetime parsing
    # Extract date using regular expression
    date_match = re.search(r': (.+)$', input_string)
    if date_match:
        date_str = date_match.group(1)
    else:
        date_str = None

    try:
        # First, try to parse with abbreviated month name format (%b)
        try:
            date = datetime.strptime(date_str, '%b %d, %Y')
        except ValueError:
            # If that fails, try with full month name format (%B)
            date = datetime.strptime(date_str, '%B %d, %Y')
    except ValueError:
        # If that also fails, return None for both values
        date = None

    return version, date


url = "https://support.google.com/chrome/a/answer/10314655"

# Send an HTTP GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table containing Chrome OS versions
    table = soup.find("table", class_="nice-table")

    if table:
        # Find all rows in the table except the header
        rows = table.find_all("tr")[1:]

        print("Chrome OS Versions:")
        for row in rows:
            # Extract version number from the second cell of each row
            cells = row.find_all("td")
            raw_text = cells[0].get_text().strip()
            version, date = extract_version_and_date(raw_text)
            if version and date:
                print("Version:", version)
                print("Date:", date.strftime('%Y-%m-%d'))
                print("url:", "https://support.google.com/chrome/a/answer/10314655#" + version)
            else:
                print("Pattern not found in the input string.")



            #raw_text = cells[1].get_text().strip()
            #print(raw_text)
            print("######################################")

else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
