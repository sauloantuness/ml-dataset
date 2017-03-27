import sqlite3
import requests
from bs4 import BeautifulSoup

USER_URL = 'https://www.urionlinejudge.com.br/judge/en/rank'
INITIAL_PAGES = 21
TOTAL_PAGES = 50


conn = sqlite3.connect('dataset.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    position INTEGER,
    university TEXT,
    solved INTEGER
)''')


def insert_user(user):
    print (user)
    c.execute('''INSERT OR REPLACE INTO user VALUES
                 (:id, :position, :university, :solved)''', user)
    conn.commit()


for page in range(INITIAL_PAGES, TOTAL_PAGES):
    print ('Page %d of %d ' % (page, TOTAL_PAGES))
    response = requests.get(USER_URL, params={'page': page})
    soup = BeautifulSoup(response.text, 'html.parser')
    for tr in soup.find('table').find_all('tr')[1:]:
        tds = tr.find_all('td')
        user = {}

        user['position'] = tds[0].text
        user['id'] = tds[2].a.attrs['href'].split('/')[-1]
        user['university'] = tds[3].a.attrs['href'].split('/')[-1]
        user['solved'] = int(tds[4].text.strip().replace(',', ''))

        insert_user(user)

conn.close()
