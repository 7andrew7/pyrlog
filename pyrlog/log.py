from abc import ABCMeta, abstractmethod

class Log(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def append(self, tpl):
        """Write a tuple to the log.

        Log writes have ACID semantics.
        """

    @abstractmethod
    def __len__(self):
        """Return the length of the log."""

    @abstractmethod
    def __iter__(self):
        """Return an iterator over the log.

        Not to be used concurrently with append invocations.
        """



