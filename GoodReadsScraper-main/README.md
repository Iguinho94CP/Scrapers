# Goodreads Quote Scraper
This Python script uses Selenium and BeautifulSoup to scrape quotes and their authors from the Goodreads website. The scraped data is then stored in an SQLite database.

## Dependencies
This script requires the following Python packages:

selenium,
BeautifulSoup, and
sqlite3
In addition, you will need to download a web driver for Selenium. The script is currently set up to use the Chrome web driver, but you can modify it to use a different web driver if needed.

## Usage
To use this script, simply run it using Python:

python3 goodreads_quotes.py

The script will then start scraping quotes from the Goodreads website and storing them in an SQLite database named quotes.db. The script will scrape quotes from 20 pages by default, but you can modify this by changing the range of the for loop in the script.

If an error occurs during scraping or storing data, the script will print an error message to the console.

## How it Works
The script opens a web browser using Selenium and navigates to the Goodreads website.
The script uses BeautifulSoup to parse the HTML of the page and extract the quotes and their authors.
The script stores the scraped data in an SQLite database.
The script clicks the "Next" button to go to the next page of quotes, and repeats steps 2-3 for each page.
Once all the data has been scraped and stored, the script closes the web browser and ends.
## Limitations
This script is designed to scrape quotes from the Goodreads website, but it may not work correctly if the website changes its structure or layout. In addition, the script may be blocked by Goodreads if too many requests are made too quickly. If you encounter any issues, you may need to modify the script or use a different scraping approach.

