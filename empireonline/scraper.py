'''
Date: 24/04/2023
UPATE-DATE: 07/05/2023
version: 2.0
Type: News scraper
Developed by: Igor Pantaleão
'''


from bs4 import BeautifulSoup
import requests
import sqlite3
import time


def requesting(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')
	return soup 

def scraping(soup):
    base_img_url = "https:"
    base_link = "https://www.empireonline.com"
    # Find the elements you want to extract text from
    cards = soup.find_all('div', {'class': 'jsx-2979979908 content'})

    news_list = []
    for card in cards:
        card_small = card.find_all('div', {'class': 'jsx-2519753491 card card-small'})
        for element in card_small:
            # Extract the news title, handling the AttributeError if it occurs
            try:
                news_title = element.find('h3', {'class': 'jsx-2519753491'}).text.replace('\n', ' ').strip()
                news_link = element.find('a')['href']
                full_link = base_link + str(news_link)
                news_category = element.find('p', {'class': 'jsx-2519753491 type-date'})
                news_category_link = base_link + str(news_category.find('a')['href'])
                news_description = element.find('div', {'class': 'jsx-2519753491 top'})
                description = news_description.find('a', {'class': 'description'}).text.replace('\n', ' ')
                publish_time = element.find('span', {'class': 'jsx-2519753491 date'}).text

                img_tags = element.find_all('img')
                img_url = ''
                for img in img_tags:
                    img_url = img['data-src']
                    full_img_url = 'https:' + img_url.replace('w=150', 'w=1200').replace('w=750', 'w=1200')

                news_dict = {
                    'Title': news_title,
                    'News_URL': full_link,
                    'News_category': news_category_link,
                    'Description': description,
                    'Image_URL': full_img_url,
                    'Publish_time': publish_time
                }

                news_list.append(news_dict)

            except AttributeError as e:
                print(f"An error occurred {e}")

    return news_list


def connect_database(db_uri):
    try:
        conn = sqlite3.connect(db_uri)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT  NOT NULL,
                news_url TEXT  NOT NULL,
                news_category TEXT  NOT NULL,
                description TEXT  NOT NULL,
                image_url TEXT  NOT NULL,
                publish_time TEXT
            )
        """)
        conn.commit()
        return conn
    except sqlite3.Error as error:
        print("Failed to connect to database", error)
        return None

def insert_to_database(news_list, db_uri):
    conn = None
    try:
        conn = sqlite3.connect(db_uri)
        cur = conn.cursor()

        # Get set of image URLs that are already in the database
        cur.execute("SELECT image_url FROM news")
        db_image_urls = {row[0] for row in cur.fetchall()}

        # Get set of image URLs in the news list
        news_image_urls = {news_dict['Image_URL'] for news_dict in news_list}

        # Insert news that have not already been inserted
        for news_dict in news_list:
        	cur.execute("""
			    INSERT INTO news (title, news_url, news_category, description, image_url, publish_time) 
			    VALUES (?, ?, ?, ?, ?, ?)
			""", (
			    news_dict['Title'], 
			    news_dict['News_URL'], 
			    news_dict['News_category'], 
			    news_dict['Description'], 
			    news_dict['Image_URL'], 
			    news_dict['Publish_time']
			))


        conn.commit()
        print(f"Successfully inserted {len(news_list)} rows into the database.")
    except sqlite3.Error as error:
        print("Failed to insert into database:", error)
    finally:
        if conn:
            conn.close()





if __name__ == "__main__":
	PATH = "/home/igor/myprojects/scrapers/movie_news_sites/empireonline/news.db"
	conn = connect_database(PATH)

	for page in range(1, 6):
		url = f'https://www.empireonline.com/movies/{page}'
		soup = requesting(url)
		time.sleep(1.5)

		
		
		news = scraping(soup)
		insert_to_database(news, PATH)

	conn.close()


