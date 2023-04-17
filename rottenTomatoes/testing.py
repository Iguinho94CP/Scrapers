from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd


driver = webdriver.Chrome()
driver.get('https://editorial.rottentomatoes.com/all-time-lists')
current_url = driver.current_url

# THIS FUNCTION ITERATE THROUGH THE FIRST PAGE ELEMENTS
time.sleep(5)


def get_news_data():
    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_item_divs = soup.select(
        'div.col-sm-8.newsItem.col-full-xs a.unstyled.articleLink')

    for news_item_div in news_item_divs:
        href_link = news_item_div['href']
        column_pic = news_item_div.find('img')['src']
        news_title = news_item_div.find('p').text
        news_pub_date = news_item_div.find(
            'p', {'class': 'publication-date'}).text
        data = {
            'Article_title': news_title,
            'Article_publication_date': news_pub_date,
            'Article_image': column_pic,
            'Article_url': href_link
        }

    return data


# THIS CODE HERE NEEDS TO BE UPDATED SO IT WILL CLICK ON ALL 15 THUMBS.
for i in range(1, 4):
    time.sleep(10)
    try:
        thumb = driver.find_element(
            By.XPATH, f'//*[@id="wpv-view-layout-1773-CATTR9a61a7f98d435e1c32de073e05574776"]/div[{i}]/div[1]/a/div[2]/div/p[1]')
        thumb.click()
    except Exception as e:
        print(e)

    # THE CURRENT URL AFTER THE THUMB ABOVE IS CLICKED
    current_URL = driver.current_url

    # WILL THESE FUNCTIONS get_movie_data(), get_movie_info_dict() and get_all_data() NEED TO BE UPDATED TOO?
    time.sleep(5)

    def get_movie_data():
        response = requests.get(current_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        movies = soup.select_one('#row-index-1')
        movie_title = movies.find('h2').find('a').text
        movie_url = movies.find('h2').find('a')['href']
        movie_year = movies.find(
            'span', {'class': 'subtle start-year'}).text.replace('(', '').replace(')', '')
        movie_score_tomatoes = movies.find(
            'span', {'class': 'tMeterScore'}).text
        critics_consensus = movies.find(
            'div', {'class': 'info critics-consensus'}).text.strip()
        movie_synopsis = movies.find(
            'div', {'class': 'info synopsis'}).text.strip()

        movie = {
            'Movie_title': movie_title,
            'Movie_year': movie_year,
            'Movie_score': movie_score_tomatoes,
            'Movie_url': movie_url,
            'Critics_consensus': critics_consensus,
            'Movie_synopsis': movie_synopsis
        }
        return movie

    movie_data = get_movie_data()
    movie_url = movie_data['Movie_url']

    driver.get(movie_url)
    time.sleep(5)

    def get_movie_info_dict():
        response = requests.get(movie_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        label_map = {
            "Director:": "Director",
            "Producer:": "Producer",
            "Writer:": "Writer",
            "Release Date (Theaters):": "Release Date (Theaters)",
            "Release Date (Streaming):": "Release Date (Streaming)",
            "Box Office (Gross USA):": "Box Office (Gross USA)",
            "Runtime:": "Runtime",
            "Distributor:": "Distributor",
            "Production Co:": "Production Co",
            "Sound Mix:": "Sound Mix",
            "Aspect Ratio:": "Aspect Ratio",
        }

        info_dict = {}

        try:
            info_ul = soup.find('ul', {'id': 'info'})
            info_items = info_ul.find_all('li', {'class': 'info-item'})

            for i in info_items:
                label = i.find("b", {"class": "info-item-label"})
                value = i.find("span", {"class": "info-item-value"})

                if label and value:
                    label_text = label.text.strip()
                    value_text = value.text.strip().replace('\n', '').replace('  ', '')

                    if label_text in label_map:
                        key = label_map[label_text]
                        info_dict[key] = value_text

        except:
            print("An error occurred while parsing movie information.")

        return info_dict

    def get_all_data():

        data = {
            **get_news_data(),
            **get_movie_data(),
            **get_movie_info_dict()
        }
        return data

        all_data = get_all_data()
        df = pd.DataFrame([all_data])
        df.to_csv('rotten_tomatoes.csv', index=False)

    driver.back()
    driver.back()
