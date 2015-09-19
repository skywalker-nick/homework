def deco(func):

    def _deco():
        print("before myfunc() called.")
        func()
        print("after myfunc() called.")

    return _deco

@deco
def myfunc(a):
    print("myfunc() called. %s" % a)

myfunc('abc')
