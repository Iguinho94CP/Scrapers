from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_pendrive_info(search, page: int) -> List[Dict[str, Optional[str]]]:
    url = f"https://pt.aliexpress.com/w/wholesale-{search}.html?SearchText={search}&catId=0&initiative_id=SB_20230430151811&spm=a2g0o.home.1000002.0&trafficChannel=main&g=y&page={page}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    pendrives = soup.find_all('a', {'class': 'manhattan--container--1lP57Ag cards--gallery--2o6yJVt'})

    return [{
            'product_title': pendrive.find('h1', {'class': 'manhattan--titleText--WccSjUS'}).text.strip(),
            'price': pendrive.find('div', {'class': 'manhattan--price-sale--1CCSZfK'}).text.strip() if pendrive.find('div', {'class': 'manhattan--price-sale--1CCSZfK'}) is not None else None,
            'quantity_sold': pendrive.find('span', {'class': 'manhattan--trade--2PeJIEB'}).text.strip() if pendrive.find('span', {'class': 'manhattan--trade--2PeJIEB'}) is not None else None,
            'rating': pendrive.find('span', {'class': 'manhattan--evaluation--3cSMntr'}).text.strip() if pendrive.find('span', {'class': 'manhattan--evaluation--3cSMntr'}) is not None else None
            } for pendrive in pendrives]


# create a list of dictionaries containing pendrive info for all pages
data = [item for page in range(1, 11) for item in scrape_pendrive_info("mouse", page)]

# create a DataFrame from the data list
df = pd.DataFrame(data)

# save the DataFrame to a CSV file with a unique name
timestamp = pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"mouses_{timestamp}.csv"
df.to_csv(filename, index=False)