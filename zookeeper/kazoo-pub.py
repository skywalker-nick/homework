import random
import kazoo
from kazoo.client import KazooClient
from kazoo.handlers.eventlet import SequentialEventletHandler
from kazoo.retry import KazooRetry
from kazoo.recipe.watchers import ChildrenWatch
from oslo_serialization import jsonutils

_handler = SequentialEventletHandler()
_retry = KazooRetry(max_tries=3, delay=0.5, backoff=2,
                    sleep_func=_handler.sleep_func)
client = KazooClient(hosts='192.168.163.129:2181',
                     handler=_handler,
                     timeout=30,
                     connection_retry=_retry)

#import pdb
#pdb.set_trace()

abc = {'name': '99'}
node = str(random.randint(10, 1000))

client.start()
lports = client.get_children('/openstack/lport/')
# client.create('/openstack/lport/%s' % node, jsonutils.dumps(abc))

for lport in lports:
    value,state = client.get('/openstack/lport/%s' % lport)
    json_val = jsonutils.loads(value)
    if json_val['name']:
        json_val['name'] = str(int(json_val['name']) + 1)
    else:
        json_val['name'] = '0'
    client.set('/openstack/lport/%s' % lport, jsonutils.dumps(json_val))
    print "%s: %s" % (lport, json_val['name'])

