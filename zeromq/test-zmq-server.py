#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
from eventlet.green import zmq

context = zmq.Context(1)
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv_multipart()
    print "hello: %s\n" % len(message)
    for i in message:
        print("Received: %s" % len(i))

    #  Do some 'work'
    time.sleep(1)

