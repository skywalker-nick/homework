import etcd
import time

client = etcd.Client(host='192.168.138.121', port=4001)
client.write('/nodes/n1', 1)
client.write('/nodes/n2', 2)
client.write('/nodes/n3', 3)

time.sleep(10)

mod_obj = client.read('/nodes/n2').value
print mod_obj
