"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test


    def test_srv_getMiro(self):  # each test_* function is a test
        """Test get miro"""
        msg = self.client.get("Miro")
        self.assertEqual(msg, '12345')

    def test_srv_getBjoern(self):  # each test_* function is a test
        """Test get Björn"""
        msg = self.client.get("Björn")
        self.assertEqual(msg, '4545454')

    def test_srv_getBjoern(self):  # each test_* function is a test
        """Test get Björn"""
        msg = self.client.get("Björn2")
        self.assertEqual(msg, 'null')

    def test_srv_getBjoern(self):  # each test_* function is a test
        """Test get Björn"""
        msg = self.client.getall()
        self.assertEqual(msg, "{\"Miro\": \"12345\", \"Tim\": \"54321\", \"Björn\": \"4545454\"}") 

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
