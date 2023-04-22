# IMDB Movie Scraper
This Python code allows you to scrape information about movies from the IMDB website using the Selenium and BeautifulSoup libraries.

### Installation
To run this code, you will need to install the following libraries:

- selenium
- pandas
- beautifulsoup4
- requests

### Usage
To use the code, simply run the imdb_scraper.py file. The code will open a new Chrome window and navigate to the IMDB website. It will then click through to the Advanced Title Search page and select various search criteria (such as release date, rating, and language) to narrow down the results.

Once the search is complete, the code will scrape information about each movie listed on the search results pages. This includes the movie title, year, genre, rating, description, duration, director, cast, gross, and image URL.

The information for all pages will be stored in a pandas DataFrame called imdb_df. By default, the code will scrape information for the first 1000 movies (i.e., the first four pages of results with 250 movies per page). You can change this by modifying the range(1, 5) line in the for loop.

### License
This code is licensed under the MIT license.
