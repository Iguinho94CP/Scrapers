import sqlite3
import time
from functools import lru_cache
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@lru_cache(maxsize=None)
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(options=options)

def create_database():
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 summary TEXT,
                 author TEXT,
                 image TEXT)''')

    conn.commit()
    conn.close()

def scrape_website(url):
    # Initialize the webdriver
    driver = get_driver()

    # Load the website
    driver.get(url)

    time.sleep(5)

    while True:
        # Scroll down to the bottom of the page
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # Find the 'Next Page' button and click it
            try:
                next_page_button = driver.find_element_by_xpath('/html/body/main/section[2]/div/section/a')
                next_page_button.click()
                time.sleep(5)
            except:
                # If there is no 'Next Page' button, break out of the loop
                break
        last_height = new_height

    # Wait for the page to load completely
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sentinel-listing-page-list')))

    # Retrieves the page source
    page_source = driver.page_source

    # Parse the page source using bs4
    soup = BeautifulSoup(page_source, 'html.parser')

    listing_page = soup.find('div', {'class': 'sentinel-listing-page-list'})

    titles = [t.text.replace('\n', '').strip() for t in soup.find_all('h5', {'class': 'display-card-title'})]

    summary = [s.text.replace('\n', '').strip() for s in soup.find_all('p', {'class': 'display-card-excerpt'})]

    author = [a.text.strip() for a in soup.find_all('a', {'class': 'display-card-author'})]

    # Find all the <figure> tags in the page
    figure_tags = soup.find_all('figure')

    # Loop over all the <figure> tags and extract the links from the <source> tags
    images = []
    for figure_tag in figure_tags:
        source_tags = figure_tag.find_all('source')
        for source_tag in source_tags:
            srcset = source_tag.get('srcset')
            sources = srcset.split(',')
            for source in sources:
                if source.startswith('https'):
                    images.append(source.strip())

    # Connect to the database
    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()

    # Insert data into the table
    for i in range(len(titles)):
        c.execute("INSERT INTO articles (title, summary, author, image) VALUES (?, ?, ?, ?)",
                  (titles[i], summary[i], author[i], images[i]))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Close the webdriver
    driver.quit()

if __name__ == '__main__':
    create_database()
    scrape_website('https://screenrant.com/comics-news/')
