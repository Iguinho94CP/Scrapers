
# Screenrant Comics 

This is a Python script that scrapes the website [Screenrant](https://screenrant.com/comics-news/) for the latest comics news and saves the data to a SQLite database.

## Requirements
- Python 3.x
- Selenium
- Beautiful Soup 4
- ChromeDriver

## Installation

> - Clone the repository to your local machine.
> - Install the dependencies using pip install -r requirements.txt.
> - Install ChromeDriver from [here](https://chromedriver.chromium.org/downloads) and add it to your PATH.

### Usage
> - Open your terminal and navigate to the repository.
> - Run python screenrant_comics_scraper.py to start the scraper.
> - The script will scrape the website and save the data to a SQLite database named mydatabase.db in the same directory as the script.

### Notes
> - The script uses an LRU cache to cache the webdriver instance, which helps to speed up the script.
> - The script uses Selenium to scroll down to the bottom of the page and load all the articles.
> - The script then uses Beautiful Soup 4 to parse the HTML and extract the titles, summaries, authors, and images for each article.
> - The script saves the data to a SQLite database using the create_database() function and the scrape_website() function.
> - The database table is named articles and has the columns id, title, summary, author, and image.