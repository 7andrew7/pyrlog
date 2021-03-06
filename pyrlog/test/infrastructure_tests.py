
import unittest

from pyrlog.test.fake_node import *
from pyrlog.test import *

import gevent

"""Tests of the simulation infrastructure."""

def run_instance(node, func):
    """Execute a client or server function; exit on termination."""
    func(node)
    node.exit()

class InfrastructureTests(unittest.TestCase):
    DURATION  = 1000

    def setUp(self):
        self.clock = FakeClock()
        self.network = FakeNetwork()

        self.nodes = [FakeNode(i, self.network, self.clock, self.DURATION)
                      for i in range(2)]
        self.server = self.nodes[0]
        self.client = self.nodes[1]

    def __run(self, server_run, client_run):
        gevent.joinall([
            gevent.spawn(run_instance, self.server, server_run),
            gevent.spawn(run_instance, self.client, client_run)
            ], raise_error=True)

    def test_client_server(self):
        def server_run(node):
            print 'SERVER RUN'

            src, msg = node.receive(block=True)
            print 'SERVER MSG'
            self.assertEqual(src, 1)
            node.send(src, msg + 1)

            print 'SERVER BYE'

        def client_run(node):
            print 'CLIENT RUN'

            node.send(0, 17)
            src, msg = node.receive(timeout=1000)
            print 'CLIENT MSG'

            self.assertEqual(src, 0)
            self.assertEqual(msg, 18)

            print 'CLIENT BYE'

        self.__run(server_run, client_run)

    def test_timeout(self):
        def run(node):
            with self.assertRaises(NodeTimeout):
                src, message = node.receive(block=False, timeout=100)

        self.__run(run, run)

    def test_deadlock(self):
        def run(node):
            src, msg = node.receive(block=True)

        with self.assertRaises(gevent.hub.LoopExit):
            self.__run(run, run)

    def test_end_of_test(self):
        def run(node):
            with self.assertRaises(EndOfTest):
                while True:
                    src, msg = node.receive(block=False, timeout=self.DURATION * 10)

        self.__run(run, run)
