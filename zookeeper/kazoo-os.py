import kazoo
from kazoo.client import KazooClient
#from kazoo.handlers.eventlet import SequentialEventletHandler
from kzeventlet.handler import SequentialEventletHandler
from kazoo.retry import KazooRetry

_handler = SequentialEventletHandler()
_retry = KazooRetry(max_tries=3, delay=0.5, backoff=2,
                    sleep_func=_handler.sleep_func)
client = KazooClient(hosts='192.168.138.121:2181',
                     handler=_handler,
                     timeout=30,
                     connection_retry=_retry)

#import pdb
#pdb.set_trace()

client.start()
client.ensure_path('/openstack')
client.ensure_path('/openstack/lswitch')

client.create('/openstack/lswitch/3', 'abc', makepath=True)
