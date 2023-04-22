# Bing scraper - Scraping actor movies
This project aims to scrape information about actor movies from the Bing search engine using Python's Selenium and BeautifulSoup libraries.

## Required Libraries:
- Selenium
- BeautifulSoup
- Requests

## Description:
> - This Python script starts by opening a Bing search engine and searching for a given actor's name. It then clicks on the movies link on the search results page and extracts the top three movies of the actor. The script then navigates to each movie page and clicks on the cast link to extract the top three cast members. Finally, for each of these cast members, the script navigates to their movie page and extracts the top three movies they were in.

## Functionality:
> - Opens a web browser and navigates to Bing search engine.
> - Searches for the given actor's name.
> - Clicks on the movies link on the search results page and extracts the top three movies.
> - Navigates to each movie page and clicks on the cast link to extract the top three cast members.
> - For each of the cast members, navigates to their movie page and extracts the top three movies they were in.
> - Stores the extracted data in a list of dictionaries.
## Usage:
> - Replace the value of the string variable with the name of the actor you want to search for.
> - Run the script.
> - The script will print out the extracted data.
## Limitations:
> - This script is designed to work only on the Bing search engine. It may not work on other search engines.
> - This script may not work if the HTML structure of the search engine pages changes.