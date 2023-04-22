from bs4 import BeautifulSoup as bs
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get('https://www.goodreads.com/quotes')
driver.implicitly_wait(10)

html = driver.page_source

try:
    # create connection to database
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()

    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS quotes
                 (quote TEXT, author TEXT)''')

    for i in range(20):
        soup = bs(html, 'html.parser')
        for quote in soup.select('div.quoteText'):
            q = quote.text.strip().split('\n')[0]
            author = quote.select_one('span.authorOrTitle').text.strip()
            # insert data into table
            c.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (q, author))
            print(f'Inserted {q} by {author}')
        next_button = driver.find_element(By.XPATH, '//a[@class="next_page"]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)
        html = driver.page_source
    # commit changes and close connection
    conn.commit()
    conn.close()

except Exception as e:
    print(f'Error: {e}')

driver.quit()

