from pyroute2 import IPDB
from pyroute2 import NetNS
from pyroute2.common import uifname

ip = IPDB(nl=NetNS('ns1'))

def test1():
    try:
        device = ip.interfaces['veth0']['ipaddr']
    finally:
        pass

for i in range(1000):
    test1()

ip.release()
