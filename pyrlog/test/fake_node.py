from pyrlog.node import Node
from gevent.queue import Queue

"""A System implementation appropriate for local unit tests."""

class FakeClock(object):
    def __init__(self):
        self._fake_time = 1
        self._alarms = [] # Time of next clock expiration for each node

    def increment(self):
        """Increment fake time.

        Return a list of node indexes whose timer has expired.
        """
        self._fake_time += 1
        
        return [idx for idx, alarm in self._alarms if alarm <= self._fake_time]

    def add_node(self):
        self._alarms.append(10000000)

    def get_time(self):
        return self._fake_time

class FakeNetwork(object):
    def __init__(self):
        self._all_nodes = []
        self._in_flight_messages = Queue()

    def add_node(self, node):
        self._all_nodes.append(node)

    def __iadd__(self, node):
        self._all_nodes.append(node)

    def __get__item(self, idx):
        return self._all_nodes[idx]

    def __len__(self):
        return len(self._all_nodes)

class FakeNode(Node):

    def __init__(self, node_id, network, clock):
        Node.__init__(self)

        self._node_id = node_id
        self._network = network
        self._clock = clock
        self._queue = Queue()

        clock.add_node()
        network.add_node(self)

    @property
    def node_id(self):
        return self._node_id
    
    @property
    def num_nodes(self):
        return len(self._network)
    
    def receive(self, timeout=0):
        pass

    def send(self, dest_id, message):
        """Send a message to a given destination."""
        self._network[dest_id]._queue.put((self.node_id, message))

    def time(self):
        """Returns seconds since the epoch."""
        return self._clock.get_time()
