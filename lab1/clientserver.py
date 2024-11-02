"""
Client and server using classes
"""

import logging
import socket
import json

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

# pylint: disable=logging-not-lazy, line-too-long

class Server:
    """ The server """
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True
    
    number_dict = {"Miro": '12345', "Tim": "54321", "Björn": "4545454"}

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        """ Serve echo """
        self.sock.listen(1)
        while self._serving:  # as long as _serving (checked after connections or socket timeouts)
            try:
                # pylint: disable=unused-variable
                (connection, address) = self.sock.accept()  # returns new socket and address of client
                while True:  # forever
                    data = connection.recv(1024)  # receive data from client
                    self._logger.info(data)
                    if not data:
                        break  # stop if client stopped
                    msg = data.decode('unicode-escape')
                    if msg == "getall":
                        connection.send(json.dumps(self.number_dict).encode('ascii'))
                    else:
                        if msg.split(':')[1] in self.number_dict.keys():
                            connection.send(self.number_dict.get(msg.split(':')[1]).encode('ascii'))
                        else: 
                            connection.send("null".encode('ascii'))
                connection.close()  # close the connection
            except socket.timeout:
                pass  # ignore timeouts
        self.sock.close()
        self._logger.info("Server down.")


class Client:
    """ The client """
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        """ Call server """
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def close(self):
        """ Close socket """
        self.sock.close()

    def get(self, name=""):
        self.sock.send(("get:" + name).encode('unicode-escape'))
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('unicode-escape')
        return msg_out
    
    def getall(self):
        self.sock.send("getall".encode('unicode-escape'))
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('unicode-escape')
        return msg_out
