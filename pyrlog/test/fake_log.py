from pyrlog.log import *

"""Memory-backed Log implementation."""

class FakeLog(Log):
    def __init__(self):
        self._entries = []

    def append(self, entries, offset):
        self._entries[offset:] = entries

    def __len__(self):
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)

    def __eq__(self, other):
        return self._entries == other._entries
