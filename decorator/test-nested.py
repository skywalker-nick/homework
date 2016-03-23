import lockdb

@lockdb.wrap_db_lock()
def a():
    print 'call a'


@lockdb.wrap_db_lock()
def b():
    print 'call b'
    a()


@lockdb.wrap_db_lock()
def c():
    print 'call c'
    b()


c()
