import networkx as nx
from models import User, InfectionGraph
import unittest

class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.graph = InfectionGraph()
        User(graph=self.graph)._reset_id_gen()
        self.alice = User(name='Alice', graph=self.graph)
        self.bob = User(name='Bob', version='red', graph=self.graph)

    def testCreateUser(self):
        self.assertEqual(self.alice.name, 'Alice')
        self.assertEqual(self.alice.version, 'green')
        self.assertEqual(self.bob.version, 'red')
        self.assertEqual(self.alice.id, 0)
        self.assertEqual(self.bob.id, 1)

    def testAddedNodes(self):
        self.assertEqual(self.graph.nodes(), [0,1])
        self.assertEqual(self.graph.node[0]['user'], self.alice)
        self.assertEqual(self.graph.node[1]['user'], self.bob)

    @classmethod
    def tearDownClass(self):
        self.graph.clear()
        User(graph=self.graph)._reset_id_gen()

if __name__ == '__main__':
    unittest.main()
