import etcd
import time

client = etcd.Client(host='192.168.138.121', port=4001)

client.write('/nodes/n1', 2)
print 'write 2'
client.write('/nodes/n1', 3)
print 'write 3'
client.write('/nodes/n1', 4)
print 'write 4'

while(True):
    val = client.read('/nodes/n1').value
    print 'read: ' + val
