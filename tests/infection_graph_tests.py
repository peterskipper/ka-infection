import networkx as nx
from models import User, InfectionGraph
import unittest

class TestInfectionGraph(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.graph = InfectionGraph()
        User(graph=self.graph)._reset_id_gen()
        self.alice = User(name='Alice', graph=self.graph)
        self.bob = User(name='Bob', graph=self.graph)
        self.carol = User(name='Carol', graph=self.graph)
        self.dave = User(name='Dave', graph=self.graph)
        self.graph.add_connection(self.alice, self.bob)
        self.graph.add_connection(self.alice, self.carol)


    def testAddEdge(self):
        self.assertEqual(self.graph.degree(0), 2)
        self.assertEqual(self.graph.degree(1), 1)
        self.assertEqual(self.graph.degree(2), 1)
        self.assertEqual(self.graph.degree(3), 0)
        links = [sub for sub in nx.connected_components(self.graph)]
        self.assertEqual(len(links), 2)
        self.assertTrue([0,1,2] in links)
        self.assertTrue([3] in links)
        enid = 5
        self.assertRaises(AttributeError, self.graph.add_connection(
            self.alice, enid))
        self.assertRaises(AttributeError, self.graph.remove_connection(
            self.bob, enid))
        
    @classmethod
    def tearDownClass(self):
        self.graph.clear()
        User(graph=self.graph)._reset_id_gen()
