#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

from eventlet.green import zmq

context = zmq.Context(1)

buffer = []
for i in range(10000):
    buffer.append('Hello, world: %s\n' % str(i))

#  Socket to talk to server
print("Connecting to hello world server ...")
global socket
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5555")

def send(sock, buf):
    #  Do 1 requests, waiting each time for a response
    for request in range(1):
        print("Sending request %s ..." % request)
        tracker = sock.send_multipart(buf, copy=False, track=True)
        while(True):
            print("Is socket completed? %s." % str(tracker.done))
            if tracker.done:
                return '\nDONE!!!!!!!!!!!!\n'

print send(socket, buffer)
