import networkx as nx 
from models import User, InfectionGraph
import unittest
from collections import namedtuple

class TestInfection(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.graph = InfectionGraph()
        User(graph=self.graph)._reset_id_gen()
        self.alice = User(name='Alice', graph=self.graph)
        self.bob = User(name='Bob', graph=self.graph)
        self.carol = User(name='Carol', graph=self.graph)
        self.dave = User(name='Dave', graph=self.graph)
        self.enid = User(name='Enid', graph=self.graph)
        self.frank = User(name='Frank', graph=self.graph)
        self.grace = User(name='Grace', graph=self.graph)
        self.henry = User(name='Henry', graph=self.graph)
        self.iris = User(name='Iris', graph=self.graph)
        self.jack = User(name='Jack', graph=self.graph)
        self.kate = User(name='Kate', graph=self.graph)
        self.larry = User(name='Larry', graph=self.graph)
        self.mia = User(name='Mia', graph=self.graph)
        self.ned = User(name='Ned', graph=self.graph)
        self.ophelia = User(name='Ophelia', graph=self.graph)
        self.pedro = User(name='Pedro', graph=self.graph)
        self.quinn = User(name='Quinn', graph=self.graph)
        self.ray = User(name='Ray', graph=self.graph)
        self.sally = User(name='Sally', graph=self.graph)
        self.tom = User(name='Tom', graph=self.graph)
        self.uma = User(name='Uma', graph=self.graph)

        self.all_users = [self.alice, self.bob, self.carol, self.dave, 
            self.enid, self.frank, self.grace, self.henry, self.iris, 
            self.jack, self.kate, self.larry, self.mia, self.ned, self.ophelia,
            self.pedro, self.quinn, self.ray, self.sally, self.tom, self.uma]

        Conn = namedtuple('Conn', 'user1 user2')
        all_conns = [Conn(self.alice, self.bob),
            Conn(self.alice, self.carol),
            Conn(self.dave,self.enid),
            Conn(self.enid, self.frank),
            Conn(self.enid, self.grace),
            Conn(self.enid, self.henry),
            Conn(self.jack, self.kate),
            Conn(self.jack, self.larry),
            Conn(self.kate, self.mia),
            Conn(self.kate, self.ned),
            Conn(self.larry, self.ophelia),
            Conn(self.larry, self.pedro),
            Conn(self.larry, self.quinn),
            Conn(self.ray, self.sally),
            Conn(self.ray, self.tom),
            Conn(self.ray, self.uma),
            ]
        self.graph._add_mult_conns(all_conns)

    def testInfectGroup(self):
        for user in [self.alice, self.bob, self.carol]:
            self.assertEqual(user.version, 'green')
        self.graph.infect_group(version='red', group=[0,1,2])
        for user in [self.alice, self.bob, self.carol]:
            self.assertEqual(user.version, 'red')

        # Switch 'em back    
        self.graph.infect_group(version='green', group=[0,1,2])

    def testTotalInfection(self):
        for user in self.all_users:
            self.assertEqual(user.version, 'green')

        self.graph.total_infection('red', self.dave)
        for user in self.all_users[3:8]:
            self.assertEqual(user.version, 'red')
        for user_id in range(3,8):
            self.assertEqual(self.graph.node[user_id]['user'].version, 'red')
        
        # Check that no one else changed
        for user in self.all_users[0:3] + self.all_users[8:]:
            self.assertEqual(user.version, 'green')
        for user_id in range(0,3) + range(8,21):
            self.assertEqual(self.graph.node[user_id]['user'].version, 'green')

        # Switch one more group
        self.graph.total_infection('red', self.ophelia)
        for user in self.all_users[3:8] + self.all_users[9:17]:
            self.assertEqual(user.version, 'red')
        for user_id in range(3,8) + range(9,17):
            self.assertEqual(self.graph.node[user_id]['user'].version, 'red')

        # Check that no one else changed
        for user in self.all_users[0:3] + self.all_users[8:9] + self.all_users[17:]:
             self.assertEqual(user.version, 'green')
        for user_id in range(0,3) + range(8,9) + range(17,21):
            self.assertEqual(self.graph.node[user_id]['user'].version, 'green')

        # Switch everyone back
        self.graph.total_infection('green', self.dave)
        self.graph.total_infection('green', self.ophelia)

    @classmethod
    def tearDownClass(self):
        self.graph.clear()
        User(graph=self.graph)._reset_id_gen()
