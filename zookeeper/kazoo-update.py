import time

from kazoo.client import KazooClient
from kazoo.client import KazooState

import logging
logging.basicConfig()

def my_listener(state):
    if state == KazooState.LOST:
    # Register somewhere that the session was lost
        print 'The session is lost: %s' % str(state)
    elif state == KazooState.SUSPENDED:
    # Handle being disconnected from Zookeeper
        print 'The session is suspended: %s' % str(state)
    else:
    # Handle being connected/reconnected to Zookeeper
        print 'The session is reconnected: %s' % str(state)

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
zk.add_listener(my_listener)

# Ensure a path, create if necessary
zk.ensure_path("/dragonflow/table1")

# Determine if a node exists
if zk.exists("/dragonflow/table1/key1"):

    # Do transaction
    transaction = zk.transaction()
    transaction.create('/dragonflow/table1/key9', b"value9")
    transaction.set_data('/dragonflow/table1/key1', b"value8")
    results = transaction.commit()

    print(results)

result = zk.get('/dragonflow/table1/key8')
print result[0]
