import zmq
import random
import sys
import threading
import time

port = "5556"

class PubThread(threading.Thread):
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%s" % port)
        while True:
            topic = random.randrange(9999,10005)
            messagedata = random.randrange(1,215) - 80
            socket.send("%d %d" % (topic, messagedata))
            print "sending: %d %d" % (topic, messagedata)
            time.sleep(1)


class SubThread(threading.Thread):
    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect ("tcp://localhost:%s" % port)
        topicfilter = "10001"
        socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        while True:
            string = socket.recv()
            topic, messagedata = string.split()
            print "recving: %s %s" % (topic, messagedata)

if __name__ == "__main__":
    p1 = PubThread()
    p2 = SubThread()
    p1.start()
    p2.start()

    while True:
        time.sleep(1)
