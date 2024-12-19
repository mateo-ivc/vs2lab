import sys
import time
import zmq
import const

context=zmq.Context()

#receive from splitter
receiver=context.socket(zmq.PULL)
receiver.connect("tcp://" + const.LOCALHOST + ":" + const.SPLITTERPORT)

#reducer
red1 = context.socket(zmq.PUSH)
red1.connect("tcp://" + const.LOCALHOST + ":" + const.PORT1)
red2 = context.socket(zmq.PUSH)
red2.connect("tcp://" + const.LOCALHOST + ":" + const.PORT2)

reducer1 = 0
reducer2 = 0
while True:
    line = receiver.recv_string()
    for word in line.split():
        if word[0].isupper():
            red1.send_string(word)
            reducer1+=1
        else:
            red2.send_string(word)
            reducer2+=1
        print(f"Send to Reducer 1: {reducer1} | Send to Reducer 2: {reducer2}")
    