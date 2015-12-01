from neutron.agent.linux import ip_lib
from neutron.agent.linux import utils

root_helper = 'sudo neutron-rootwrap /etc/neutron/rootwrap.conf'
ip = ip_lib.IPWrapper()

# ip -o -d link list
# return name list
def test1():
    try:
        ip_lib.device_exists('eth0')
    finally:
        pass

for i in range(1000):
    test1()
