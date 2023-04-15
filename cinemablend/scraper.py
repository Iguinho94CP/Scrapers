from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
import sqlite3


chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.cinemablend.com/")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, 'homePageCarousel')))


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


def scraping(soup, db_file):
    # Find all feature block sections
    feature_blocks_section = soup.find_all('section', {'class': 'feature-block'})

    # Initialize empty list to store the extracted data
    data = []

    # Extract data from each feature block
    for feature in feature_blocks_section:
        for i in range(1, 8):
            class_name = f'feature-block-item-wrapper item-{i}'
            article_name_elem = feature.find('div', class_name)
            span = article_name_elem.find('span').text.strip()
            link = article_name_elem.find('a')['href']
            img_tag = article_name_elem.find('img')
            if img_tag:
                srcset = img_tag['srcset']
                urls = srcset.split(',')
                for url in urls:
                    if re.search(r'-650-80\.jpg', url.strip()):
                        image_url = url.strip().split(' ')[0]
                        data.append((span, link, image_url))

    # Save the extracted data to a SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS articles (article_name TEXT, link TEXT, image_url TEXT)')
    c.executemany('INSERT INTO articles VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

# Example usage
db_file = 'news.db'
scraping(soup, db_file)