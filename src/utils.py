import gzip
import networkx as nx
import matplotlib.pyplot as plt

def load_edges(file_path):
    with gzip.open(file_path, 'rt') as f:
        edges = []
        for line in f:
            u, v = map(int, line.split())
            edges.append((u, v))
    return edges

def load_clusters(file_path):
    with gzip.open(file_path, 'rt') as f:
        clusters = {}
        for line in f:
            node, cluster = map(int, line.split())
            if cluster not in clusters:
                clusters[cluster] = []
            clusters[cluster].append(node)
    return list(clusters.values())

def export_to_gephi(edges, clusters, output_file):
    G = nx.Graph()
    G.add_edges_from(edges)

    # Assign clusters as node attributes
    cluster_map = {node: i for i, cluster in enumerate(clusters) for node in cluster}
    nx.set_node_attributes(G, cluster_map, "Cluster")

    # Write to GEXF file
    nx.write_gexf(G, output_file)
    print(f"Graph exported to {output_file}")

def debug(A, D, diam, P, m_k_all):
    print("\nAdjecency Matrix A:\n", A)
    print("\nDistance Matrix D:\n", D, "\nDiameter: ", diam)
    print("\nPaths Matrix P:\n", P)
    print("\nTotal number of shortest paths m_k: ", m_k_all)

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