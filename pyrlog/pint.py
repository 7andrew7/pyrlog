from abc import ABCMeta, abstractmethod

class PersistentInteger(object):
    """This class represents a persistent integer.

    All operations have ACID semantics.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self):
        """Return the integer value."""

    @abstractmethod
    def set(self, val):
        """Set the integer value."""

    @abstractmethod
    def increment(self):
        """Increment the value by one; return new value."""
