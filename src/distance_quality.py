import numpy as np
import networkx as nx

from utils import debug

# adjacency matrix A
def adj(edges, n):
    A = np.zeros((n, n), dtype=int)
    for u, v in edges:
        A[u, v] = A[v, u] = 1
    return A

# powers of adjacency matrix A^k
def adj_k(A, k):
    return np.linalg.matrix_power(A, k)

# distance matrix D
def distance(A):

    G = nx.from_numpy_array(A, create_using=nx.Graph)
    distances = dict(nx.all_pairs_shortest_path_length(G))

    # n+1 distance if there is no path
    n = A.shape[0]
    D = np.full((n, n), fill_value=n + 1, dtype=int)
    
    for i in range(n):
        for j in range(n):
            if j in distances[i]:
                D[i, j] = distances[i][j]
    
    return D

# paths matrix P
def paths(A):
    n = A.shape[0]
    G = nx.from_numpy_array(A, create_using=nx.Graph)
    P = np.zeros((n, n), dtype=int)
    
    shortest_path_lengths = dict(nx.all_pairs_shortest_path_length(G))
    
    for source in range(n):
        for target in range(n):
            if source == target:
                # one path from a node to itself (no self loops)
                P[source, target] = 1
            elif target in shortest_path_lengths[source]:
                # number shortest paths between source and target
                all_paths = list(nx.all_shortest_paths(G, source=source, target=target))
                P[source, target] = len(all_paths)
            else:
                # no path between source and target (disconnected)
                P[source, target] = 0

    return P

# generalized degree d_k(v)
def k_degree(v, P, D, k):
    return np.sum(P[v, D[v] == k])

# total number of shortest paths m_k
def total_shortest_paths(P, D, k):
    # 0.5 to avoid double counting
    return 0.5*np.sum([k_degree(v, P, D, k) for v in range(len(D))])

# probability Pr[i, j, k]
def probability(i, j, k, P, D, m_k):
    d_i_k = k_degree(i, P, D, k)
    d_j_k = k_degree(j, P, D, k)
    
    return (d_i_k / (2*m_k)) * (d_j_k / (2*m_k))
    

# expected distance D_V(i, j)
def expected_distance(i, j, diam, P, D, m_k_all):
    expected_dist = 0
    for k in range(1, diam+1):
        expected_dist += k*probability(i, j, k, P, D, m_k_all[k - 1])

    return expected_dist

# sum expected distances in cluster C
def expected_distances_C(C, diam, P, D, m_k_all):
    
    total_dist = np.sum([expected_distance(i, j, diam, P, D, m_k_all) for i in C for j in C if i != j])
    return total_dist / 2

# sum observed distances in cluster C
def observed_distances_C(C, D):
    total_dist = np.sum([D[i, j] for i in C for j in C if D[i, j] < D.shape[0]+1])
    return total_dist / 2

# Distance Quality Function Q_d
def distance_quality_function(G, clusters):
    A = adj(G['edges'], G['n'])
    D = distance(A)
    P = paths(A)

    diam = np.max(D[D < G['n'] + 1])
    m_k_all=[total_shortest_paths(P, D, k) for k in range(1, diam + 1)]

    debug(A, D, diam, P, m_k_all)

    Q_d = 0
    for C in clusters:
        expected = expected_distances_C(C, diam, P, D, m_k_all)
        observed = observed_distances_C(C, D)
        Q_d += (observed - expected)
    return Q_d