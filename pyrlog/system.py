from abc import ABCMeta

class System(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def receive(timeout=10):
        """Blocking message receive.

        :param timeout: The maximum number of seconds to block.
        :return: A tuple of (node_id, message) or None on timeout.
        """

    @abstractmethod
    def send(node_id, message):
        """Send a message to a given destination."""


    @abstractmethod
    def time():
        """Returns seconds since the epoch."""
