from abc import ABCMeta, abstractmethod

class Log(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def append(self, entries, offset):
        """Write entries to the log.

        :param entries: A list of log entries.
        :param offset: Offset within the log.  Must be <= len(log).

        Log writes have ACID semantics.
        """

    @abstractmethod
    def __len__(self):
        """Return the length of the log."""

    def last_index(self):
        """Return the index of the last log entry."""
        return len(self) - 1

    @abstractmethod
    def __iter__(self):
        """Return an iterator over the log.

        Not to be used concurrently with append invocations.
        """
