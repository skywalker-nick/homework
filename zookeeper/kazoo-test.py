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
    # Do something
    
    # Print the version of a node and its data
    data, stat = zk.get("/dragonflow/table1/key1")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    # List the children
    children = zk.get_children("/dragonflow/table1")
    print("There are %s children with names %s" % (len(children), children))

    # Update the data
    zk.set("/dragonflow/table1/key1", b"value2")

    # Print the version of a node and its data
    data, stat = zk.get("/dragonflow/table1/key1")
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
else:
    zk.create("/dragonflow/table1/key1", b"value1")

@zk.ChildrenWatch("/dragonflow/table1")
def watch_children(children):
    print("Children are now: %s" % children)
    # Above function called immediately, and from then on

@zk.DataWatch("/dragonflow/table1/key1")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

while(1):
    time.sleep(1)
    print("Waiting...\n")
