import sys
import os
import networkx as nx
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from test import test

G = nx.Graph()
edges = [
    (0, 1), (0, 2), (0, 3),
    (1, 3), (1, 4),
    (2, 3),
    (3, 4),
    (4, 5),
]
G.add_edges_from(edges)
test(G, k=2)