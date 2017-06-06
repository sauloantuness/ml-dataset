import random


print 'user,problem,category,date'

users = list(range(1000))
problems = list(range(1001, 1500))

for user in users:
	num_problems = int(random.random() * len(problems))

	user_problems = problems[:num_problems]
	for date, problem in enumerate(user_problems):
		print '%d,%d,1,%03d' % (user, problem, date)
