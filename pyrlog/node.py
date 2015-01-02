from abc import ABCMeta, abstractmethod

class NodeTimeout(Exception):
    pass

class Node(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def receive(self, block=False, timeout=0):
        """Blocking message receive.

        :param block: Whether to block waiting for a response.
        :param timeout: If non-blocking, the maximum timeout length.
        :return: A tuple of (node_id, message).

        Raises a Timeout exception on a timeout.
        """

    @abstractmethod
    def send(self, dest_id, message):
        """Send a message to a given destination."""

    @abstractmethod
    def time(self):
        """Returns seconds since the epoch."""
