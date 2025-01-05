import numpy as np
import networkx as nx
from utils import debug

# Distance matrix D
def distance(G):
    n = len(G.nodes)
    D = np.full((n, n), fill_value=np.inf, dtype=float)
    
    for source, target_lengths in nx.all_pairs_shortest_path_length(G):
        for target, length in target_lengths.items():
            D[source, target] = length
    
    return D

# Paths matrix P
def paths(G):
    n = len(G.nodes)
    P = np.zeros((n, n), dtype=int)
    
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                try:
                    all_paths = list(nx.all_shortest_paths(G, source=source, target=target))
                    P[source, target] = len(all_paths)
                except nx.NetworkXNoPath:
                    P[source, target] = 0
    return P

# Generalized degree d_k(v)
def k_degree(v, P, D, k):
    return np.sum(P[v, (D[v] == k)])

# Total number of shortest paths m_k
def total_shortest_paths(P, D, k):
    return 0.5 * np.sum([k_degree(v, P, D, k) for v in range(len(D))])

# Probability Pr[i, j, k]
def probability(i, j, k, P, D, m_k):
    d_i_k = k_degree(i, P, D, k)
    d_j_k = k_degree(j, P, D, k)
    if m_k == 0:  # Avoid division by zero
        return 0
    return (d_i_k / (2 * m_k)) * (d_j_k / (2 * m_k))

# Expected distance D_V(i, j)
def expected_distance(i, j, diam, P, D, m_k_all):
    expected_dist = 0
    for k in range(1, diam + 1):
        if m_k_all[k - 1] > 0:  # Avoid division by zero
            expected_dist += k * probability(i, j, k, P, D, m_k_all[k - 1])
    return expected_dist

# Sum expected distances in cluster C
def expected_distances_C(C, diam, P, D, m_k_all):
    total_dist = np.sum([
        expected_distance(i, j, diam, P, D, m_k_all)
        for i in C for j in C
        if i != j and not np.isinf(D[i, j])  # Exclude disconnected pairs
    ])
    return total_dist / 2

# Sum observed distances in cluster C
def observed_distances_C(C, D):
    total_dist = np.sum([
        D[i, j]
        for i in C for j in C
        if i != j and not np.isinf(D[i, j])  # Exclude disconnected pairs
    ])
    return total_dist / 2

# Distance Quality Function Q_d
def distance_quality_function(G, clusters):
    P = paths(G)
    D = distance(G)
    
    # Calculate the diameter excluding infinite distances
    finite_distances = D[np.isfinite(D)]
    diam = int(np.max(finite_distances)) if len(finite_distances) > 0 else 0
    
    # Total shortest paths for each distance k
    m_k_all = [total_shortest_paths(P, D, k) for k in range(1, diam + 1)]

    # Debug information
    # debug(D, diam, P, m_k_all)

    Q_d = 0
    for C in clusters.values():
        expected = expected_distances_C(C, diam, P, D, m_k_all)
        observed = observed_distances_C(C, D)
        Q_d += expected - observed
    return Q_d