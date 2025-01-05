import networkx as nx

from networkx.algorithms.community import modularity, greedy_modularity_communities
from distance_quality import distance_quality_function
from optimal_clustering import optimal_clustering, all_clusters, convert_clusters
from utils import plot_graph

def test(G, k):
    DQ_clusters = optimal_clustering(G, k)
    QM_clusters = greedy_modularity_communities(G)

    DQ_clusters_readable = {int(k): list(v) for k, v in DQ_clusters.items()}
    QM_clusters_readable = [list(cluster) for cluster in QM_clusters]
    print("Modularity Clusters: ", QM_clusters_readable)
    print("Distance   Clusters: ", DQ_clusters_readable)

    clusters_list = convert_clusters(DQ_clusters)
    modularity_score = modularity(G, clusters_list)

    distance_quality = distance_quality_function(G, DQ_clusters)
    if nx.is_connected(G):
        print("Connected: YES\n")
    else:
        print("Connected: NO\n")

    print("Modularity Q_m: {:.2f}".format(modularity_score))
    print("Distance Quality Function Q_d: {:.2f}\n".format(distance_quality))

    A = nx.adjacency_matrix(G).todense()
    plot_graph(A)