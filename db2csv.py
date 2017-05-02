import sqlite3
from datetime import datetime


conn = sqlite3.connect('dataset.db')
c = conn.cursor()

c.execute('''SELECT * from solution''')
for problem, user, date in c.fetchall():
	d = datetime.strptime('2/25/15, 6:15:09 PM','%m/%d/%y, %I:%M:%S %p')
	print str(user) + ',' + str(problem) + ',' + d.strftime('%m/%d/%y')

conn.close()