import xml.etree.ElementTree as ET
import urllib.request
import sqlite3


def requesting(url):
    # Download the RSS feed
    
    response = urllib.request.urlopen(url)
    rss_data = response.read()

    return rss_data

def scraping(rss_data):
    # Parse the XML data
    root = ET.fromstring(rss_data)

    # Extract the channel title and description
    channel = root.find("channel")
    title = channel.find("title").text
    description = channel.find("description").text

    # Extract the items
    items = []
    for item in channel.findall("item"):
        item_data = {
            "title": item.find("title").text,
            "description": item.find("description").text.strip(),
            "link": item.find("link").text,
            "pubDate": item.find("pubDate").text,
            "image_url": item.find("enclosure").get('url')
        }
        try:
            item_data["director"] = item.find("{http://purl.org/dc/elements/1.1/}creator").text.strip()
        except AttributeError:
            item_data["director"] = None
        items.append(item_data)

    return items

def connect_database(db_path):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS movie_news (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                director TEXT NOT NULL,
                link TEXT NOT NULL,
                pub_date TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        """)
        conn.commit()
        print("Database connected.")
        return conn
    except sqlite3.Error as error:
        print("Failed to connect to database:", error)
        return None

def insert_to_database(items, conn):
    try:
        cur = conn.cursor()

        # Insert news that have not already been inserted
        for item in items:
            cur.execute("""
                INSERT INTO movie_news (title, description, director, link, pub_date, image_url) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item['title'], 
                item['description'], 
                item['director'],
                item['link'], 
                item['pubDate'],
                item['image_url']
            ))

        conn.commit()
        print(f"Successfully inserted {len(items)} rows into the database.")
    except sqlite3.Error as error:
        print("Failed to insert into database:", error)

if __name__ == "__main__":
    url = "https://movieweb.com/feed/movie-news/"
    rss_data = requesting(url)
    items = scraping(rss_data)

    db_path = "movie_news.db"
    conn = connect_database(db_path)
    if conn is not None:
        insert_to_database(items, conn)
        conn.close()