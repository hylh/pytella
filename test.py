#!/usr/bin/env python

import argparse
import httplib
from timeit import default_timer as timer
import multiprocessing as mp

class NodeTest(object):
    """ Connection to nodes for test purposes """
    def __init__(self):
        self.conn = httplib.HTTPConnection(HOSTNAME, PORT)

    def run(self):
        """ Run several different tests """
        self.test_failed_get()
        for _ in range(0, NUMBER_OF_NODES):
            proc = mp.Process(target=self.test_post_addnode)
            proc.start()
            #self.test_post_addnode()
        self.test_get()
        #self.test_post_shutdown()

    def test_failed_get(self):
        """ The get request should fail """
        print "--- Failed GET test"
        status, _ = self.request("GET", "/neighbours")
        if status == 404:
            print "Test passed"
        return

    def test_post_addnode(self):
        """ Test the addNode function """
        print "--- addNode Test"
        _, res = self.request("POST", "/addNode")
        print "Result:", res
        return

    def test_get(self):
        """ The get request should pass """
        print "\n--- GET Test"
        status, res = self.request("GET", "/neighbours")
        print "Status code:", status
        print "Result:", res
        if status == 200:
            print "GET response OK!"
        return

    def test_post_shutdown(self):
        """ Test the shutdown of a node """
        print "\n--- shutdown Test"
        status, res = self.request("POST", "/shutdown")
        print "Status code:", status
        print "Result:", res
        return

    def request(self, method, path, payload=None):
        """ Create a http request """
        self.conn.request(method, path, payload)
        response = self.conn.getresponse()
        status = response.status
        data = response.read()
        response.close()
        self.conn.close()
        return status, data

def parse_args():
    """ Parse command line arguments """
    default_nodes = 5
    default_host = "localhost"
    default_port = 8000

    parser = argparse.ArgumentParser(prog="test",
            description="Test of starting nodes")

    parser.add_argument("-n", "--num_nodes", type=int, default=default_nodes,
            help="how many nodes to start, default %d" % default_nodes)

    parser.add_argument("-host", "--hostname", type=str, default=default_host,
            help="which node to connect to")

    parser.add_argument("-p", "--port", type=int, default=default_port,
            help="which port to use, default %d" % default_port)

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_args()
    NUMBER_OF_NODES = ARGS.num_nodes
    HOSTNAME = ARGS.hostname
    PORT = ARGS.port
    NODE_TEST = NodeTest()

    START = timer()
    NODE_TEST.test_get()
    END = timer()
    print "TEST used: %.4f seconds" % (END - START)