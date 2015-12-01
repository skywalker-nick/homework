from pyroute2 import IPDB
from pyroute2.common import uifname

ip = IPDB()

def test1():
    try:
        device = ip.interfaces['eth0']['ipaddr']
    finally:
        pass

for i in range(1000):
    test1()

ip.release()
