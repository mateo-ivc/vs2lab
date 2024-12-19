import zmq
import sys
import const
import json

context = zmq.Context()

port = str(sys.argv[1])

receiver = context.socket(zmq.PULL)
receiver.bind("tcp://" + const.LOCALHOST +":"+ port)

map = {}
while True:
    word = receiver.recv_string()
    if word not in map:
        map[word] = 1
    else:
        map[word] += 1
    print(json.dumps(map, indent=4))