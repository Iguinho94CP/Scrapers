import sqlite3
import requests
from bs4 import BeautifulSoup


class JobDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                skills TEXT NOT NULL,
                category TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def add_job(self, data):
        self.cur.execute("""
            INSERT INTO jobs (url, title, location, skills, category)
            VALUES (?, ?, ?, ?, ?)
        """, (data['Job URL'], data['Job Title'], data['Job Location'], data['Skills'], data['Category']))
        self.conn.commit()

    def close(self):
        self.conn.close()


url = "https://www.python.org/jobs/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

jobs = soup.find_all('li')

job_db = JobDatabase('jobs.db')

for job in jobs:
    base_url = 'https://www.python.org'
    try:
        data = {
            'Job URL': base_url + job.find('span', {'class':'listing-company-name'}).find('a')['href'],
            'Job Title': job.find('span', {'class': 'listing-company-name'}).text.strip().replace('\n', '').replace('\t', ''),
            'Job Location': job.find('span', {'class':'listing-location'}).text.strip(),
            'Skills': job.find('span', {'class': 'listing-job-type'}).text.strip(),
            'Category': job.find('span', {'class':'listing-company-category'}).text
        }
        job_db.add_job(data)

    except AttributeError:
        pass

job_db.close()
