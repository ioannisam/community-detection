import numpy as np
import itertools
import networkx as nx
from sklearn.cluster import KMeans
from distance_quality import distance_quality_function

# finds the optimal clustering for a dataset to maximize the distance quality function
def optimal_clustering(G, k):
    A = nx.adjacency_matrix(G).todense()

    # K-means clustering
    kmeans = KMeans(n_clusters=k, random_state=0).fit(A)
    labels = kmeans.labels_
    
    # clusters dictionary
    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(i)
    
    return clusters

# calculates Qd for all possible clusterings of k clusters
def all_clusters(G, k):
    best_clustering = {}
    best_Q_d = -np.inf

    # all possible clusterings with exactly k clusters
    for clustering in itertools.product(range(k), repeat=G.number_of_nodes()):
        clusters = {i: [] for i in range(k)}
        for node, cluster_id in enumerate(clustering):
            clusters[cluster_id].append(node)
        
        Q_d = distance_quality_function(G, clusters)
        if Q_d > best_Q_d:
            best_Q_d = Q_d
            best_clustering = clusters
    
    return best_clustering

# converts clusters dictionary to list of lists
def convert_clusters(clusters):
    return [nodes for nodes in clusters.values()]