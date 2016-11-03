import eventlet
import kazoo
from kazoo.client import KazooClient
from kazoo.handlers.eventlet import SequentialEventletHandler
from kazoo.retry import KazooRetry
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.recipe.watchers import DataWatch
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

client.start()

@client.ChildrenWatch('/openstack/lport/')
def func(children):
    print children

def data_change(data, stat):
    print "data: %s" % data
    print "stat: %s" % stat
    return True

@client.DataWatch('/openstack/lport/')
def data_change1(data, stat):
    print "data: %s" % str(data)
    print "stat: %s" % str(stat)
    return True

global_watches = {}

lports = client.get_children('/openstack/lport/')
for lport in lports:
    value,state = client.get('/openstack/lport/%s' % lport)
    global_watches[lport] = DataWatch(client, '/openstack/lport/%s', data_change)

print global_watches

while(True):
    eventlet.sleep(1)
