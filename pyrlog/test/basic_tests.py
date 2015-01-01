
import unittest

from pyrlog.test.fake_node import *
from pyrlog.test import *
from pyrlog.message import *

import gevent

class PyrlogTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.network = FakeNetwork()

        node = FakeNode(0, self.network, self.clock)

        self.nodes = [FakeNode(i, self.network, self.clock) for i in range(7)]
        self.servers = self.nodes[:5]
        self.clients = self.nodes[5:]

    def test_client_server(self):
        def server_run(node):
            src, msg = node.receive(1000)
            self.assertEquql(msg[0], MESSAGE_OP)
            self.assertEqual(src, len(self.servers))

            node.send(src, (MESSAGE_OP_RESPONSE, msg[1] + 1))

        def client_run(node):
            node.send((MESSAGE_OP, 17))
            src, msg = node.receive(10)
            self.assertEqual(src, 0)
            self.assertEqual(msg[0], MESSAGE_OP_RESPONSE)
            self.assertEqual(msg[1], 18)


        gevent.joinall([
            gevent.spawn(server_run, self.servers[0]),
            gevent.spawn(client_run, self.clients[0])
        ])
