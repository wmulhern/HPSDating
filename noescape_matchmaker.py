import socket
import sys
import numpy as np
from dating.utils import floats_to_msg4
import scipy.spatial.distance as ds

orig_candidates = []
opp_candidates = []
orig_scores = []
opp_scores = []

PORT = int(sys.argv[1])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', PORT))

num_string = sock.recv(4)
assert num_string.endswith('\n')

num_attr = int(num_string[:-1])

for i in range(20):
    data = sock.recv(8 + 2*num_attr)
    print "Score: ", float(data[0:7])
    orig_scores.append(float(data[0:7]))
    orig_candidates.append(map(int, data[8:].split(',')))
    opp_scores.append(-1 * float(data[0:7]))
    opp_candidates.append([(x+1)%2 for x in map(int, data[8:].split(','))])
    assert data[-1] == '\n'

print min([abs(y) for y in orig_scores])
print max([abs(y) for y in orig_scores])


# Now have all 40 things. How to extract info????

for i in range(20):
    a = np.random.random(num_attr)
    sock.sendall(floats_to_msg4(a))

    data = sock.recv(8)
    assert data[-1] == '\n'
    score = float(data[:-1])
    print('i = %d score = %f' % (i, score))

sock.close()