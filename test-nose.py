def compute(a, b):
    return a + b

def Test1():
    a = -1
    b = 1
    assert compute(a, b) == -1

def testabc():
    a = 0
    b = -1
    assert compute(a, b) == 0

def Test3():
    a = 1
    b = 10
    assert compute(a, b) == 10

def Test4():
    a = -1
    b = -1
    assert compute(a, b) == 1
