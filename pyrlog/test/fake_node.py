from pyrlog.node import Node, NodeTimeout
from gevent.queue import Queue

"""A System implementation appropriate for local unit tests."""

class FakeClock(object):
    def __init__(self):
        self._fake_time = 1

    def increment(self):
        """Increment fake time."""
        self._fake_time += 1
        return self.get_time()

    def get_time(self):
        return self._fake_time

    def set_time(self, tm):
        assert(tm >= self._fake_time)
        self._fake_time = tm
        return self._fake_time

class FakeNetwork(object):
    def __init__(self):
        self._all_nodes = []

    def add_node(self, node):
        self._all_nodes.append(node)

    def __iadd__(self, node):
        self._all_nodes.append(node)

    def __getitem__(self, idx):
        return self._all_nodes[idx]

    def __len__(self):
        return len(self._all_nodes)

    def __iter__(self):
        return iter(self._all_nodes)

class FakeNode(Node):

    TIMEOUT = "TIMEOUT"

    def __init__(self, node_id, network, clock):
        Node.__init__(self)

        self._node_id = node_id
        self._network = network
        self._clock = clock
        self._alarm = 0 # No pending alarm
        self._queue = Queue()

        network.add_node(self)

    @property
    def node_id(self):
        return self._node_id
    
    @property
    def num_nodes(self):
        return len(self._network)
    
    def receive(self, block=False, timeout=0):
        time = self._clock.increment()

        if block:
            self._alarm = 0
        else:
            self._alarm = time + timeout

        print '[%d] %d RX' % (self._clock.get_time(), self._node_id)

        no_pending_messages = all(node._queue.empty() for node in self._network)
        if no_pending_messages:
            # Advance time to guarantee that some node's timer fires
            try:
                soonest_alarm = min(node._alarm for node in self._network
                                    if node._alarm > 0)
                time = self._clock.set_time(max(self._clock.get_time(), soonest_alarm))
            except ValueError:
                pass # No pending alarms; hopefully we're not deadlocked...

        for node in self._network:
            alarm = node._alarm
            if alarm > 0 and alarm <= time and node._queue.empty():
                print '  [%d] ALARM %d' % (self._clock.get_time(), node.node_id)
                node._queue.put(FakeNode.TIMEOUT)

        print '%d %d QUEUE wait' % (self._node_id, id(self))
        result = self._queue.get()
        print '%d QUEUE wakeup' % self._node_id

        if result is FakeNode.TIMEOUT:
            raise NodeTimeout()
        else:
            return result

    def send(self, dest_id, message):
        """Send a message to a given destination."""
        dest_node = self._network[dest_id]
        print '[%d] SEND %d ==> %d %d %d' % (self._clock.get_time(), self._node_id, dest_id,
            dest_node._node_id, id(dest_node))
        dest_node._queue.put((self._node_id, message))

    def time(self):
        """Returns seconds since the epoch."""
        return self._clock.get_time()
