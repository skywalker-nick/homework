import etcd
import time

client = etcd.Client(host='192.168.138.121', port=4001)
client.write('/nodes/n1', 1)
client.write('/nodes/n2', 2)
client.write('/nodes/n3', 3)

lock = client.get_lock('/nodes/n1', ttl=60)
with lock as mylock:
    val = client.read('/nodes/n1').value
    print 'read in lock: ' + val
    time.sleep(15)
    newval = int(val) + 99
    client.write('/nodes/n1', newval)
    print 'write in lock: ' + newval
