import kazoo
from kazoo.client import KazooClient
from kazoo.handlers.eventlet import SequentialEventletHandler
from kazoo.retry import KazooRetry

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

