
"""Definition of message types.

All pyrlog messages are pickle-encoded tuples, whose first element is an
integer from among this set.
"""

MESSAGE_OP = 1
MESSAGE_OP_RESPONSE = 2
