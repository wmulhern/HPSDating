import random
import numpy as np

attr_num = 20


player = [0] *  attr_num

neg_sum = 0
pos_sum = 0

for i in range(attr_num):
	pos_flag = random.random() > 0.5
	val = random.random() * 0.5
	if pos_sum == 1:
		pos_flag = False
	if neg_sum == 1:
		if not pos_flag and pos_sum != 1:
			pos_flag = True
		else:
			break
	if pos_flag:
		pos_max = 1 - pos_sum
		if pos_max < 0.05:
			val = pos_max
		else:
			val = pos_max * val
		pos_sum += val
	else:
		neg_max = -1 - neg_sum
		if neg_max > -0.05:
			val = neg_max
		else:
			val = neg_max * val
		neg_sum += val
	player[i] = val

player = np.asarray(player)
candidates = []
for i in range(20):
	candidate = [random.random() for x in range(attr_num)]
	candidate = np.asarray(candidate)
	print "CANDIDATE",i
	print "-" * 30
	print "\t",[float("{0:.2f}".format(a)) for a in candidate]
	print "\tscore:",np.dot(player,candidate)
	print "-" * 30
	candidates.append(candidate)

print "PLAYER"
print "-" * 30
print player