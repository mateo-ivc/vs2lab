import rpc
import logging

from context import lab_logging

def returnMsg(value):
    print("Result: {}".format(value.value))

lab_logging.setup(stream_level=logging.INFO)

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
#msgrcv = self.chan.receive_from(self.server) 
result_list = cl.append('bar', base_list, returnMsg)

# print("Result: {}".format(result_list.value))

cl.stop()


    