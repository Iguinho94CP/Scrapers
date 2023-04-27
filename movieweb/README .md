
# Movie News RSS Feed Scraper
This Python script scrapes the Movie News RSS feed from [MovieWeb](https://movieweb.com/feed/movie-news/), extracts the movie news data from the XML, and inserts it into a SQLite database named movie_news.db.

## Requirements
- Python 3.x
- xml.etree.ElementTree library
- urllib.request library
- sqlite3 library
## Usage
- Clone or download the repository.
- Open a terminal or command prompt window in the directory containing the script.
- Run the script using the command python3 scraper.py.
- The script will scrape the RSS feed, extract the data, and insert it into the movie_news table in the movie_news.db database.
- If the table or database does not exist, the script will create them.
## Functions
### requesting(url)
Downloads the RSS feed from the specified url and returns the RSS data.

### scraping(rss_data)
Parses the XML data from rss_data, extracts the movie news data, and returns a list of dictionaries representing each movie news item.

### connect_database(db_path)
Connects to the SQLite database located at db_path and creates the movie_news table if it does not exist.

### insert_to_database(items, conn)
Inserts the movie news data in items into the movie_news table in the database connected to conn.

### License
This script is licensed under the MIT License.