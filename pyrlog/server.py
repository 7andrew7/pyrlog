
class Server(object):

    def __init__(self, system, local_id, num_nodes):
        self.system = system
        self.local_id = local_id
        self.num_nodes = num_nodes

        system.register_receive_handler(self)

    def do_operation(op, handler):
        """Perform an operation, as requested by a client.

        :param op: A tuple describing the operation.
        :param handler: A handler to invoke upon completion.
        """

    def receive_message(sender_id, tpl):
        """Message receive callback.

        :param sender_id: ID of the sender (an integer)
        :param tpl: The content of the Message
        """
