import etcd

client = etcd.Client(host='192.168.138.121', port=4001)
client.write('/nodes/n2', 9999)
mod_obj = client.read('/nodes/n2').value
print mod_obj
