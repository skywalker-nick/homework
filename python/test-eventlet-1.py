import time

import eventlet
eventlet.monkey_patch()

def func(n):
    print 'xxx', n
    #for i in range(1000):
    #    if i == 500:
    #        eventlet.sleep(0.01)
    #    pass

eventlet.spawn(func, 'abc')


# return

time.sleep(0)
