import itertools
import networkx as nx
from collections import namedtuple
import operator

class User(object):
    new_id = itertools.count().next
    
    def __init__(self, graph, name='', version='green'):
        self.id = User.new_id()
        self.name = name
        self.version = version
        
        #Update graph with new person
        graph.add_node(self.id, user=self)
        
    def __repr__(self):
        return 'Id: {}, Name: {}, Version: {}'.format(self.id, self.name,
            self.version)

    # Used in unit tests
    def _reset_id_gen(self):
        new_id = itertools.count().next

class InfectionGraph(nx.Graph):

    def add_connection(self, user1, user2):
        if user1.id in self and user2.id in self:
            self.add_edge(user1.id, user2.id)

    def remove_connection(self, user1, user2):
        if user1.id in self and user2.id in self:
            self.remove_edge(user1.id, user2.id)

    def total_infection(self, user):
        for group in nx.connected_component_subgraphs(self):
            if user.id in group:
                for ident in group:
                    self.node[ident]['user']['version'] = user.version
                print 'Infected {}, starting with User {}'.format(len(group), 
                    user.id)
                break

    def limited_infection(self, target, cushion):
        Subgraph = namedtuple('Subgraph', 'size first_member')
        graphs = [Subgraph(size=len(sub), first_member=sub[0]) for sub in 
            nx.connected_components(self)].sort(key=operator.itemgetter(0),
                reverse=True)
        
        add_loc = 0
        stack = [graphs[add_loc]]
        while True:
            if target - cushion < sum(sub.size for sub in stack) < target + cushion:
                for sub in stack:
                    total_infection(self, self.node[sub.first_member]['user'])
                return True # BOO-YA!

            elif sum(sub.size for sub in stack) > target + cushion:
                stack.pop()
                add_loc += 1
                if add_loc < len(graphs):
                    stack.append(graphs[add_loc])
                else:
                    return False # Quit searching

            else:
                add_loc += 1
                if add_loc < len(graphs):
                    stack.append(graphs[add_loc])
                else:
                    return False # Quit searching

