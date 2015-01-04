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

class AppendEntriesRequest(object):
    def __init__(self, prev_log_length, entries, leader_commit_count):
        self._prev_log_length = prev_log_length
        self._entries = entries
        self._leader_commit_count = leader_commit_count

class AppendEntriesResponse(object):
    def __init__(self, log_length):
        self._log_length = log_length
