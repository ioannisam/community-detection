import sys
import os
import networkx as nx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from test import test

G = nx.Graph()
edges = [
    (0, 1), 
    (1, 2), 
    (2, 3)
]
G.add_edges_from(edges)

test(G, k=1)