<h2>Background</h2>

<p>The graphs representing User relationships (coached-by or is-coached-by) is implemented using Python's NetworkX library, which uses adjacency lists to represent the graph.  Adjacency lists are generally a memory efficient way to represent this type of graph.</p>

<p>I implemented an undirected graph, because infections travel in both directions (coach to student, and vice versa).</p>


<h2>Code Examples</h2>

```python
import networkx as nx
from models import User, InfectionGraph

graph = InfectionGraph()
alice = User(name='Alice', version='green', graph=graph)
bob = User(name='Bob', version='green', graph=graph)
carol = User(name='Carol', version='green', graph=graph)
dave = User(name='Dave', version='green', graph=graph)
enid = User(name='Enid', version='green', graph=graph)

# Alice teaches Bob, Carol & Dave. Enid works on her own
graph.add_connection(alice, bob)
graph.add_connection(carol, alice)
graph.add_connection(alice, dave)


# Total Infection: will infect Alice, Bob, Carol, Dave
graph.total_infection(version='red', user=alice)

# Equivalently
graph.total_infection(version='red', user=bob)


# Limited Infection: Searches graph for subgroups that total *target*, 
# plus or minus *boundary*. Function only assigns full subgroups to the new
# version. If it cannot find a combo that is within the boundary, it returns
# False, and no groups are changed. Command below will find Alice, Bob, Carol
# & Dave and assign them the new version. 
graph.limited_infection(version='red', target=3, boundary=1)

# Exact Infection: Exhaustive search finds all subgroups, sorts them, and
# determines if any combo will exactly match *target*. If so, infects that exact
# number of users. If not, returns False (no subgroups changed).
# Code below finds Enid and infects only her:
graph.exact_infection(version='red', target=1)
```

<h2>Installation</h2>

<p>
Install dependencies from the root directory with:
</p> 
``` sh
$ pip install -r requirements.txt
```  

<h2>Tests</h2>

<p>
Run tests from the root directory with:
</p>
``` sh
$ nosetests tests
```

