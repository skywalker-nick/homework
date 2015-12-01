from neutron.agent.linux import ip_lib

root_helper = 'sudo neutron-rootwrap /etc/neutron/rootwrap.conf'
ip = ip_lib.IPWrapper()

# ip -o -d link list
# return name list
def test1():
    try:
        device = ip.device('eth0')
        ips = device.addr.list(scope='global')
    finally:
        pass

for i in range(1000):
    test1()
