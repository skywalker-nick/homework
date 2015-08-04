class TestNumber():
    var1 = 0
    var2 = 0

    def setUp(self):
        self.var1 = 1
        self.var2 = 2
        print "TestCase setup"

    def tearDown(self):
        self.var1 = 0
        self.var2 = 0
        print "TestCase teardown"

    def test_func_1(self):
        assert self.var1 == self.var2

    def test_func_2(self):
        assert self.var1 != self.var2
