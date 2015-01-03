from collections import namedtuple

"""Definition of message types."""


class RequestVoteRequest(object):
    def __init__(self, term, candidate_id, last_log_index, last_log_term):
        self._term = term
        self._candidate_id = candidate_id
        self._last_log_index = last_log_index
        self._last_log_term = last_log_term


class RequestVoteResponse(object):
    def __init__(self, term, vote_granted):
        self._term = term
        self._vote_granted = vote_granted

class AppendEntriesRpc(object):
    def __init__(self, term, leader_id):
        self._term = term
        self._leader_id = leader_id
