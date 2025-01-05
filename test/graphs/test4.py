import sys
import os
import networkx as nx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from test import test

G = nx.Graph()
edges = [
    (0, 1), 
    (2, 3),
    (4, 5)
]
G.add_edges_from(edges)
test(G, k=3)