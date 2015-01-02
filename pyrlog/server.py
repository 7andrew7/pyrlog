
class Server(object):

    def __init__(self, node, num_servers, log, current_term, voted_for):
        """Initialize a Raft server instance.

        :param node: The node that provides system services for this server.
        :param num_servers: The number of servers in the Raft group; assumed
        to have node IDs equal to: range(num_servers).
        :param log: An instance of log.Log to record tuples.
        :param current_term: An instance of PersistentInteger that records the
        latest term seen by this server.
        :param voted_for: An instance of PersistentInteger that records the
        candidate that received the vote in the current term; -1 indicates None.
        """
        self._node = node
        self._num_servers = num_servers
        self._log = log
        self._current_term = current_term
        self._voted_For = voted_for

