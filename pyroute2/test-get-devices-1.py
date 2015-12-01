from pyroute2 import IPDB
from pyroute2.common import uifname

ip = IPDB()

# ip -o -d link list
# return name list
def test1():
    try:
        iflist = filter(lambda x: type(x) is not int, ip.interfaces.keys())
    finally:
        pass

for i in range(1000):
    test1()

ip.release()
