import numpy as np
import networkx as nx
# import matplotlib.pyplot as plt

from scipy.sparse.csgraph import shortest_path

# adjacency matrix A
def adj(edges, n):
    A = np.zeros((n, n), dtype=int)
    for u, v in edges:
        A[u, v] = A[v, u] = 1
    print("\nAdjecency Matrix A:\n", A)
    return A

# powers of adjacency matrix A^k
def adj_k(A, k):
    return np.linalg.matrix_power(A, k)

# distance matrix D
def distance(A):
    D = shortest_path(csgraph=A, directed=False, unweighted=True)
    print("\nDistance Matrix D:\n", D)
    return np.array(D, dtype=int)

# paths matrix P
def paths(A, D):
    n = len(A)
    P = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            k = D[i, j]
            P[i, j] = adj_k(A, k)[i, j]
    print("\nPaths Matrix P:\n", P)
    return P

# generalized degree d_k(v)
def k_degree(v, P, D, k):
    return sum(P[v, i] for i in range(len(D)) if D[v, i] == k)

# total number of shortest paths m_k
def total_shortest_paths(P, D, k):
    return 0.5*sum(k_degree(v, P, D, k) for v in range(len(D)))

# probability Pr[i, j, k]
def probability(i, j, k, P, D, m_k):
    d_i_k = k_degree(i, P, D, k)
    d_j_k = k_degree(j, P, D, k)
    if m_k > 0:
        return (d_i_k / (2*m_k)) * (d_j_k / (2*m_k))
    return 0

# expected distance D_V(i, j)
def expected_distance(i, j, diam, P, D):
    expected_dist = 0
    for k in range(1, diam+1):
        m_k = total_shortest_paths(P, D, k)
        if m_k > 0:
            expected_dist += k*probability(i, j, k, P, D, m_k)
    return expected_dist

# sum observed distances in cluster C
def observed_distances_C(C, D):
    total_dist = 0
    for i in C:
        for j in C:
            if i != j:
                total_dist += D[i, j]
    return total_dist/2

# sum expected distances in cluster C
def expected_distances_C(C, diam, P, D):
    total_dist = 0
    for i in C:
        for j in C:
            if i != j:
                total_dist += expected_distance(i, j, diam, P, D)
    return total_dist/2

# Distance Quality Function Q_d
def distance_quality_function(G, clusters):
    A = adj(G['edges'], G['n'])
    D = distance(A)
    P = paths(A, D)
    diam = np.max(D[np.isfinite(D)])
   
    Q_d = 0
    for C in clusters:
        expected = expected_distances_C(C, diam, P, D)
        observed = observed_distances_C(C, D)
        Q_d += (expected - observed)
    return Q_d

# example
G = {
    'n': 6,
    'edges': [(0, 1), (0, 2), (0, 3), (1, 3), (1, 4), (2, 3), (3, 4), (4, 5)]
}
clusters = [[0, 1], [2, 3], [4, 5]]
print("\nDistance Quality Function Q_d:", distance_quality_function(G, clusters))

def plot_graph(A):
    G = nx.Graph()
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] != 0:
                G.add_edge(i, j)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)
    plt.show()

# A = adj(G['edges'], G['n'])
# plot_graph(A)