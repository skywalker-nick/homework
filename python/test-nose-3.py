# Module Level

def setUp():
    print 'test setup'

def tearDown():
    print 'test teardown'

# Function Level

def func_1_setup():
    print 'test_func_1 setup'

def func_1_teardown():
    print 'test_func_1_teardown'

# Target Func
def test_func_1():
    print 'test_func_1 run'
    assert True
test_func_1.setUp = func_1_setup
test_func_1.tearDown = func_1_teardown

