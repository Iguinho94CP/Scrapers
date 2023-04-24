
# Empire Online Movie News Scraper
This project is a Python script that scrapes the latest movie news from the Empire Online website and stores it in an SQLite database.

# How to Use
> 1. Clone this repository: git clone https://github.com/Iguinho94CP/empire-online-scraper.git
> 2. Install the required packages: pip install -r requirements.txt
> 3. Run the script: python main.py
The script will scrape the latest movie news from the first 20 pages of the Empire Online website and store it in an SQLite database located at file:/home/igor/myprojects/scrapers/empireonline/news.db.

# Challenges Faced
 During development, I faced the following challenges:

> 1. Pagination Problems: The pagination on the website was not consistent, which caused the scraper to miss some pages of news. I solved this by adding a loop to iterate through the pages until there were no more news articles to scrape.

> 2. Duplicates Images URLs: The scraper was not adding some news articles to the database because their image URLs were duplicates of those in the database. This issue was resolved by comparing the image URLs in the database to those in the scraped news articles and only adding articles with unique image URLs.

# Issues
> The scraper is not always able to find image URLs for the news articles, so some articles may not have an image in the database. Additionally, there may be some issues with inserting the image URLs into the database.