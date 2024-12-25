import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from distance_quality import distance_quality_function, adj
from utils import plot_graph

G = {
    'n': 6,
    'edges': [(0, 1), (0, 2), (3, 4), (4, 5)]
}
clusters = [[0, 1, 2], [3, 4, 5]]
print("Connected: NO\nClusters: 2\n")
print("\nDistance Quality Function Q_d: {:.2f}".format(distance_quality_function(G, clusters)))

A = adj(G['edges'], G['n'])
plot_graph(A)