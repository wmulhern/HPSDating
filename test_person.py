import socket
import sys
import numpy as np
from dating.utils import floats_to_msg2, candidate_to_msg


PORT = int(sys.argv[1])


def get_valid_prob(n):
    alpha = np.random.random(n)
    p = np.random.dirichlet(alpha)
    p = np.trunc(p*100)/100.0

    # ensure p sums to 1 after rounding
    p[-1] = 1 - np.sum(p[:-1])
    return p


def get_valid_weights(n):
    half = n/2

    a = np.zeros(n)
    a[:half] = get_valid_prob(half)
    a[half:] = -get_valid_prob(n - half)
    return np.around(a, 2)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', PORT))

num_string = sock.recv(4)
assert num_string.endswith('\n')

num_attr = int(num_string[:-1])

import random
import numpy as np 

pos_hold = []
neg_hold = []

#num_attr = 60

golden = 1/((1 + 5 ** 0.5) / 2)

#use golden ratio for number of positive values

pos_num = int(golden * num_attr)
neg_num = num_attr - pos_num

initial_pos_num = round(1.0/pos_num,2)
initial_neg_num = -1 * round(1.0/neg_num,2)
float(str(initial_pos_num)[:4])
max_change_pos = round(initial_pos_num * 0.8,2)
max_change_neg = round(initial_neg_num * 0.8,2)
#max_change_pos = round(float(str(max_change_pos)[:4]),2)
print max_change_pos

amount_change = pos_num/2

if pos_num % 2 != 0:
    pos_hold.append(initial_pos_num)

for i in range(amount_change):
    change = round(random.uniform(0,max_change_pos),2)
    updated_low = round(initial_pos_num - change,2)
    update_high = round(initial_pos_num + change,2)
    print change,update_high,updated_low
    pos_hold.append(update_high)
    pos_hold.append(updated_low)

while round(sum(pos_hold),2) != 1.0:
    print "entering while loop"
    print sum(pos_hold)
    value_needed = 1 - round(sum(pos_hold),2) 
    if abs(value_needed) < max_change_pos:
        change_amount = value_needed
    elif sum(pos_hold) < 1:
        change_amount = round(random.uniform(0,max_change_pos),2)
    else:
        change_amount = -1 * round(random.uniform(0,max_change_pos),2)
    random_pos_idx = random.randint(0,pos_num-1)
    if pos_hold[random_pos_idx] <= abs(change_amount) and change_amount < 0:
        print "CONTINUE",change_amount,pos_hold[random_pos_idx]
        continue
    pos_hold[random_pos_idx] = round(pos_hold[random_pos_idx] + change_amount,2)

    print sum(pos_hold)
    print "exiting?"

amount_change = neg_num/2

if neg_num % 2 != 0:
    neg_hold.append(initial_neg_num)

for i in range(amount_change):
    change = round(random.uniform(0,max_change_neg),2)
    updated_low = round(initial_neg_num - change,2)
    update_high = round(initial_neg_num + change,2)
    print change,update_high,updated_low
    neg_hold.append(update_high)
    neg_hold.append(updated_low)

while round(sum(neg_hold),2) != -1.0:
    print "entering while loop BEG"
    print sum(neg_hold)
    value_needed = -1 - round(sum(neg_hold),2) 
    if abs(value_needed) < abs(max_change_neg):
        change_amount = value_needed
    elif sum(neg_hold) < -1:
        change_amount = round(random.uniform(0,max_change_neg),2)
    else:
        change_amount = -1 * round(random.uniform(0,max_change_neg),2)
    random_neg_idx = random.randint(0,neg_num-1)
    if abs(neg_hold[random_neg_idx]) <= abs(change_amount) and change_amount < 0:
        print "CONTINUE",change_amount,neg_hold[random_neg_idx]
        continue
    neg_hold[random_neg_idx] = round(neg_hold[random_neg_idx] - change_amount,2)

    print sum(neg_hold)
    print "exiting?"


print sum(neg_hold)
print sum(pos_hold)

initial_weights = pos_hold + neg_hold

print initial_weights
print sum(initial_weights)
random.shuffle(initial_weights)

print initial_weights
print sum(initial_weights)
initial_weights = np.asarray(initial_weights)

ideal_candidate = initial_weights > 0
anti_ideal_candidate = initial_weights <= 0

sock.sendall(floats_to_msg2(initial_weights))

sock.sendall(candidate_to_msg(ideal_candidate))
sock.sendall(candidate_to_msg(anti_ideal_candidate))

for i in range(20):
    # 7 char weights + commas + exclamation
    data = sock.recv(8*num_attr)
    print data
    print('%d: Received guess = %r' % (i, data))
    assert data[-1] == '\n'
    sock.send(floats_to_msg2(initial_weights))

sock.close()
