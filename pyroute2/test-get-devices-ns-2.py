from neutron.agent.linux import ip_lib

root_helper = 'sudo neutron-rootwrap /etc/neutron/rootwrap.conf'
ip = ip_lib.IPWrapper(namespace='ns1')

# ip -o -d link list
# return name list
def test1():
    try:
        iflist = []
        for device in ip.get_devices():
            iflist.append(device.name)
    finally:
        pass

for i in range(1000):
    test1()
