import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from distance_quality import distance_quality_function, adj
from optimal_clustering import optimal_clustering, all_clusters
from utils import plot_graph, load_edges, load_clusters, export_to_gephi

edges_file = "../email-Eu-core.txt.gz"
labels_file = "../email-Eu-core-department-labels.txt.gz"

edges = load_edges(edges_file)
clusters = load_clusters(labels_file)

gephi_dir = "gephi"
if not os.path.exists(gephi_dir):
    os.makedirs(gephi_dir)
export_to_gephi(edges, clusters, "gephi/email-Eu-core.gexf")

G = {
    'n': max(max(u, v) for u, v in edges) + 1,
    'edges': edges
}

print("Edges: {}\nClusters: {}".format(len(edges), len(clusters)))
print("\nDistance Quality Function Q_d: {:.2f}".format(distance_quality_function(G, clusters)))