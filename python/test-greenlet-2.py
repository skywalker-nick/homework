import greenlet

def test1(n):
    print "test1:",n
    gr2.switch(32)
    print "test1: over"

def test2(n):
    print "test2:",n
    gr1.switch(23)
    print "test2: over"

greenlet = greenlet.greenlet
current = greenlet.getcurrent()
gr1 = greenlet(test1, current)
gr2 = greenlet(test2, current)
gr1.switch(2)
