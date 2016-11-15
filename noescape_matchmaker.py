import socket
import sys
import numpy as np
from dating.utils import floats_to_msg4
import scipy.spatial.distance as ds

orig_candidates = []
opp_candidates = []
orig_scores = []
opp_scores = []
weights = []

PORT = int(sys.argv[1])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', PORT))

num_string = sock.recv(4)
assert num_string.endswith('\n')

num_attr = int(num_string[:-1])

for i in range(20):
    data = sock.recv(8 + 2*num_attr)
    score = float(data[0:7])
    candidate = np.array(map(int, data[8:].split(',')))
    print "Score: ", score
    orig_scores.append(score)
    orig_candidates.append(candidate)
    opp_scores.append(-1 * score)
    opp_candidates.append(np.array([(x+1)%2 for x in candidate]))
    weights.append(score*candidate)
    weights.append((-1*score)*np.array([(x+1)%2 for x in candidate]))
    assert data[-1] == '\n'

weight_sum = np.zeros(num_attr)
for cand in weights:
    weight_sum += cand
print weight_sum

print min([abs(y) for y in orig_scores])
print max([abs(y) for y in orig_scores])


arr = []
for i in weight_sum:
    if i > 0:
        arr.append(1.0)
    else:
        arr.append(0.0)
print "Sending", arr
sock.sendall(floats_to_msg4(arr))

data = sock.recv(8)
assert data[-1] == '\n'
score = float(data[:-1])
print('i = %d score = %f' % (i, score))

# Now have all 40 things. How to extract info????

for i in range(19):
    a = np.random.random(num_attr)
    sock.sendall(floats_to_msg4(a))

    data = sock.recv(8)
    assert data[-1] == '\n'
    score = float(data[:-1])
    print('i = %d score = %f' % (i, score))

sock.close()