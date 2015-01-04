import random

from pyrlog.node import *
from pyrlog.message import *

"""Implementation of the Raft consistency protocol.

See: In Search of an Understandable Consensus Algorithm (Extended Version)
http://ramcloud.stanford.edu/raft.pdf
"""

class State(object):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3

class Server(object):

    KEEPALIVE_DELAY = 30
    ELECTION_DELAY = 150 # XXX not used

    def __reset_timeout(self):
        if self._state == State.LEADER:
            self._next_timeout_time = self._node.time() + KEEPALIVE_DELAY
        else:
            self._next_timeout_time = self._node.time() + ELECTION_DELAY

    def __get_receive_timeout(self):
        return self._next_timeout_time - self._node.time()

    def __reset_volatile_state(self):
        # XXX hard-coded leader
        # TODO: Leader election

        self._state = State.FOLLOWER
        if self._node.node_id == 0:
            self._state = State.LEADER

            # The leader maintains an estimate of the log length
            # at each follower; this is used to determine the number
            # of entries to send an AppendEntriesRequest:
            # entries = self._log[estimate_length:]
            log_len = len(self._log)
            self._estimated_log_length = [log_len] * self._num_servers

        # Number of log entires that have been committed and are therefore
        # safe to apply to the state machine.
        self._commit_count = -1


    def __init__(self, node, num_servers, log, current_term, voted_for):
        """Initialize a Raft server instance.

        :param node: The node that provides system services for this server.
        :param num_servers: The number of servers in the Raft group; assumed
        to have node IDs equal to: range(num_servers).
        :param log: An instance of log.Log to record tuples.
        """
        self._node = node
        self._num_servers = num_servers

        self._log = log

        # Volatile state
        self.__reset_volatile_state()

    def __broadcast(self, msg):
        """Send a message to other servers."""
        for i in range(self._num_servers):
            if i != self._node.node_id:
                self._node.send(msg)

    def __handle_message(self, src, msg):
        if isinstance(msg, AppendEntriesRequest):
            self.__reset_timeout()

            self._commit_count = min(self._commit_count,
                                     msg._leader_commit_count)
            # TODO: Apply new commits to the state machine

            if msg._prev_log_length <= len(self._log):
                self._log.append(msg.entries, msg._prev_log_length)

            response = AppendEntriesResponse(len(self._log))
            self._node.send(src, response)

        elif isinstance(msg, AppendEntriesResponse):
            self._estimated_log_length[src] = msg._log_length
            # TODO: aggressively send out new append requests for nodes with
            # holes in their log?

    def __handle_timeout(self):
        if self._state == State.LEADER:
            for i in range(self._num_servers):
                if i == self._node.node_id:
                    continue
                prev_log_length = self._estimated_log_length[i]
                new_entries = self._log[prev_log_length:]
                msg = AppendEntriesRequest(
                    prev_log_length, new_entries, self._commit_count)
                self._node.send(i, msg)
        else:
            pass # TODO: Handle leader failure here?

    def run(self):
        node = self._node

        while True:
            try:
                src, message = node.receive(self.__get_receive_timeout())
                self.__handle_message(src, message)
            except NodeTimeout:
                self.__handle_timeout()

