import sqlite3
import requests
from bs4 import BeautifulSoup

INITIAL_POSITION = 121
FINAL_POSITION = 130
USER_URL = 'https://www.urionlinejudge.com.br/judge/en/profile/'


conn = sqlite3.connect('dataset.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS solution (
    user_id INTEGER NOT NULL,
    problem_id INTEGER NOT NULL,
    date TEXT,
    PRIMARY KEY (user_id, problem_id)
)''')


def get_number_of_pages(user_id):
    response = requests.get('https://www.urionlinejudge.com.br/judge/en/profile/' + str(user_id))
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = int(soup.find(id='table-info').text.split()[-1])
    return pages


def add_solution(solution):
    print ('Problem: %s (%s)' % (solution['problem_id'], solution['date']))
    c.execute('''INSERT OR REPLACE INTO solution VALUES
                 (:user_id, :problem_id, :date)''', solution)
    conn.commit()


c.execute('''
    SELECT id, position
    FROM user
    WHERE position BETWEEN %d AND %d
    ORDER BY position''' % (INITIAL_POSITION, FINAL_POSITION))

for row in c.fetchall():
    user_id = row[0]
    position = row[1]
    user_pages = get_number_of_pages(user_id)
    print ('#%d User: %d - %d pages' % (position, user_id, user_pages))

    for page in range(1, user_pages + 1):
        print ('Page %d of %d' % (page, user_pages))
        response = requests.get(USER_URL + str(user_id), params={'page': page})
        soup = BeautifulSoup(response.text, 'html.parser')
        for tr in soup.find('table').find_all('tr')[1:]:
            tds = tr.find_all('td')

            try:
                solution = {
                    'user_id': user_id,
                    'problem_id': tds[0].text.strip(),
                    'date': tds[6].text.strip(),
                }

                add_solution(solution)
            except IndexError:
                break

conn.close()
