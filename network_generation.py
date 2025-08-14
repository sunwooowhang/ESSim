"""Network generation and analysis"""

import networkx as nx
import numpy as np

# Generate a WS graph, remember there is a seed parameter for reproducibility

def generate_ws_graph_with_info(n, k, p):
    """
    Generate a WS graph with n nodes, average degree k, and rewiring probability p.
    Return the graph, clustering coefficient, average path length, degree distribution, and small worldness
    """
    def average_ER_graph_parameters(graph_n, graph_k):
        """Given the n and k of a WS graph, compute the average parameters of the equivalent ER graph"""
        ER_p = graph_k / (graph_n - 1)

        C_values = []
        L_values = []

        for i in range(20): # 20 samples should be enough
            G_ER = nx.erdos_renyi_graph(graph_n, ER_p, seed=i)
            if nx.is_connected(G_ER):
                C = nx.average_clustering(G_ER)
                L = nx.average_shortest_path_length(G_ER)
                C_values.append(C)
                L_values.append(L)
            else:
                continue

        C_mean = np.mean(C_values)
        L_mean = np.mean(L_values)

        return C_mean, L_mean

    G = nx.watts_strogatz_graph(n, k, p)

    clustering_coefficient = nx.average_clustering(G)
    average_path_length = nx.average_shortest_path_length(G)
    degree_distribution = nx.degree_histogram(G)
    C_ER, L_ER = average_ER_graph_parameters(n, k)
    small_worldness = float((clustering_coefficient / C_ER) / (average_path_length / L_ER))

    graph_info = {
        "graph": G,
        "clustering_coefficient": clustering_coefficient,
        "average_path_length": average_path_length,
        "degree_distribution": degree_distribution,
        "small_worldness": float(small_worldness)
    }

    return graph_info

def print_graph_stats(stats_dict, round_to=4):
    """For printing the stats of the graph"""

    for key, value in stats_dict.items():
        if key == 'graph':
            continue
        if isinstance(value, float):
            print(f"{key}: {round(value, round_to)}")
        else:
            print(f"{key}: {value}")
