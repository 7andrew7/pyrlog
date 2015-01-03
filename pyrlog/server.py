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

    @staticmethod
    def choose_election_delay():
        return random.randint(150, 300)

    def accept_request_vote(self, msg):
        """Returns True if the server should accept the RequestVote message.

        See Raft[5.4.1]
        """
        if msg._term < self._current_term.get():
            return False

        if msg._last_log_term > self._log.last_term():
            return True
        if msg._last_log_term < self._log.last_term():
            return False
        return msg._last_log_index >= self._log.last_index()

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

        # Persistent state
        self._log = log
        self._current_term = current_term
        self._voted_For = voted_for

        # Volatile state
        self._state = State.FOLLOWER
        self._leader_id = -1
        self._vote_count = 0

    def __broadcast(self, msg):
        """Send a message to other servers."""
        for i in range(self._num_servers):
            if i != self._node.node_id:
                self._node.send(msg)

    def __handle_timeout(self):
        if self._state == State.FOLLOWER:
            term = self._current_term.increment()
            self._state = State.CANDIDATE
            self._vote_count = 1
            self._leader_id = -1

            msg = RequestVoteRequest(
                _self._current_term.get(), self._node.node_id,
                self._log.last_index(), self._log.last_term())
            self.__broadcast(msg)

    def __handle_message(self, src, msg):
        if isinstance(msg, RequestVoteRequest):
            grant = self.accept_request_vote(msg)
            response = RequestVoteResponse(_self._current_term.get(), grant)
            self._node.send(src, response)
        elif isinstance(msg, RequestVoteResponse):
            if msg._term > self._current_term.get():
                self._current_term.set(msg._term)

            if self._state == State.CANDIDATE:
                self._vote_count += 1
                if self._vote_count == (self._num_servers / 2 + 1):
                    self._state = State.LEADER
                    self._leader_id = self._node.node.id

                    heartbeat = AppendEntriesRequest(
                        self._current_term.get(), self._leader_id)
                    self.brodcast(heartbeat)

        elif isinstance(msg, AppendEntriesRequest):

    def run(self):
        node = self._node
        election_timeout = node.time() + choose_election_delay()
        while True:
            try:
                remaining = node.time() - election_timeout
                if remaning <= 0
                    handle_timeout()
                else:
                    src, msg = node.receive(remaning)
                    self.__handle_message(src, msg)
            except NodeTimeout:
                pass # TODO: initiate election
