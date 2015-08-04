import os

# Target Func
def rm(filename):
    os.remove(filename)

tmpfilepath = "/tmp/tmpfile"

def setUp():
    with open(tmpfilepath, "wb") as f:
        f.write("delete me")

def test_rm():
    rm(tmpfilepath)
    assert not os.path.isfile(tmpfilepath)
