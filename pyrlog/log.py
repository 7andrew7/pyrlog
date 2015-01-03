from abc import ABCMeta, abstractmethod

class Log(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def append(self, term, val):
        """Write a tuple to the log.

        :param term: The current term number; must be at least as large as
        last_term()
        :param val: The value to log.

        Log writes have ACID semantics.
        """

    @abstractmethod
    def last_term(self):
        """Return the term number of the last log entry."""

    @abstractmethod
    def last_index(self):
        """Return the index of the last log entry."""

    @abstractmethod
    def __len__(self):
        """Return the length of the log."""

    @abstractmethod
    def __iter__(self):
        """Return an iterator over the log.

        Not to be used concurrently with append invocations.
        """
