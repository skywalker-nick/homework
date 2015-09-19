def deco1(func):

    def temp():
        func()
        print("after myfunc() called.")

    print("before myfunc() called.")
    return temp

def myfunc():
    print("myfunc() called.")

myfunc = deco1(myfunc)

# calling
myfunc()
