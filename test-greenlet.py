import greenlet

def counter(n):

    p = greenlet.getcurrent().parent
    p.switch()
    for i in xrange(0, n):
        p.switch(i)




g = greenlet.greenlet(counter)
g.switch(3)

while True:
    r = g.switch()
    if r is None:
        break
    print r

