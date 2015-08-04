def deco1(func):
    print("before myfunc() called.")
    func()
    print("after myfunc() called.")

def myfunc():
    print("myfunc() called.")

deco1(myfunc)
