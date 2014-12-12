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
        self.__class__.new_id = itertools.count().next

class InfectionGraph(nx.Graph):

    def add_connection(self, user1, user2):
        try:
            self.add_edge(user1.id, user2.id)
        except AttributeError:
            print ('Cannot add connection. Either {} or {} does not have an id'
                ' Are you sure they are both users?').format(user1, user2)
    
    def _add_mult_conns(self, conn_list):
        for conn in conn_list: #conn is a namedtuple
            self.add_connection(conn.user1, conn.user2)

    def remove_connection(self, user1, user2):
        try:
            self.remove_edge(user1.id, user2.id)
        except AttributeError:
            print ('Cannot remove connection. Either {} or {} does not have '
                'an id. Are you sure they are both users?').format(
                user1, user2)

    def infect_group(self, version, group):
        for ident in group:
            self.node[ident]['user'].version = version
        print 'Infected group with {} members, including'.format(len(group),
            self.node[group[0]]['user'].name)

    def total_infection(self, version, user):
        group = nx.connected_components(self)
        while True:
            try:
                sub = group.next()
                if user.id in sub:
                    self.infect_group(version, sub)
                    break
            except StopIteration:
                print 'User {} is not in the graph! No infection'.format(user.id)

    def limited_infection(self, version, target, boundary):
        group = nx.connected_components(self)
        total = 0
        infected = []
        while total < target - boundary:
            sub = group.next()
            infected.append(sub)
            total += len(sub)
        if total < target + boundary: # Close to target
            for sub in infected:
                self.infect_group(version, sub)
                return True
        else:
            while True:
                try:
                    for i in xrange(infected):
                        temp = infected[:i] + infected[i+1:]
                        temp_total = sum(len(sub) for sub in temp)
                        if target - boundary < temp_total < target + boundary:
                            for sub in temp:
                                self.infect_group(version, sub)
                            return True
                    infected.pop()
                    infected.append(group.next())

                except StopIteration:
                    print ('Could not find a grouping at specified boundary. '
                        'Try raising boundary!')
                    return False

    def exact_infection(self, version, target):
        Subgraph = namedtuple('Subgraph', 'size members')
        graphs = [Subgraph(size=len(sub), members=sub) for sub in 
            nx.connected_components(self)].sort(key=operator.itemgetter(0),
                reverse=True)
        
        add_loc = 0
        stack = [graphs[add_loc]]
        while True:
            if sum(sub.size for sub in stack) == target:
                for sub in stack:
                    self.infect_group(version, sub.members)
                return True # BOO-YA!

            elif sum(sub.size for sub in stack) > target:
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
