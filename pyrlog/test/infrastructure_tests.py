
import unittest

from pyrlog.test.fake_node import *
from pyrlog.test import *
from pyrlog.message import *

import gevent

"""Tests of the simulation infrastructure."""

class InfrastructureTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.network = FakeNetwork()

        self.nodes = [FakeNode(i, self.network, self.clock) for i in range(2)]
        self.server = self.nodes[0]
        self.client = self.nodes[1]

    def test_client_server(self):
        def server_run(node):
            print 'SERVER RUN'

            src, msg = node.receive(block=True)
            print 'SERVER MSG'
            self.assertEqual(msg[0], MESSAGE_OP)
            self.assertEqual(src, 1)

            node.send(src, (MESSAGE_OP_RESPONSE, msg[1] + 1))

            print 'SERVER BYE'

        def client_run(node):
            print 'CLIENT RUN'

            node.send(0, (MESSAGE_OP, 17))
            src, msg = node.receive(timeout=1000)
            print 'CLIENT MSG'

            self.assertEqual(src, 0)
            self.assertEqual(msg[0], MESSAGE_OP_RESPONSE)
            self.assertEqual(msg[1], 18)

            print 'CLIENT BYE'

        gevent.joinall([
            gevent.spawn(server_run, self.server),
            gevent.spawn(client_run, self.client)
            ], raise_error=True)
