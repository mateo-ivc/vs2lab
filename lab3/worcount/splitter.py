import zmq
import re 
import time
import const

context = zmq.Context()
socket  = context.socket(zmq.PUSH)
socket.bind("tcp://"+ const.LOCALHOST +":2135")

time.sleep(40)

content=[]
# Open the file in read mode
with open('/workspaces/vs2lab/lab3/worcount/file.txt', 'r') as file:
    for line in file:
        content.append(line.strip())  
        
for index, line in enumerate(content):
    socket.send_string(line)