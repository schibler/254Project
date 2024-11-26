import networkx as nx
import random

def generate_random_dags(num_dags: int, n: int, p: float=0.1, t: int | None = None, weight_dist=lambda: random.randint(1, 10)):
    """
    Generates a series of random directed acyclic graphs (DAG).
    
    Parameters:
    - num_dags: int, the number of graphs to generate
    - n: int, number of vertices (vertices are labeled from 1 to n).
    - p: float, probability of creating an edge between two vertices (default is 0.1).
    - t: int or None, maximum allowable difference between vertices a and b for edge (a, b) (default is None, meaning any difference).
    - weight_dist: callable, a function returning weights for edges (default is random integer between 1 and 10).
    
    Returns:
    - Iterable of NetworkX directed graph (DAG) with randomly generated edges and weights.
    """

    for _ in range(num_dags):
        # Create an empty directed graph
        dag = nx.DiGraph()
        
        # Add nodes
        dag.add_nodes_from(range(1, n + 1))  # Nodes are labeled from 1 to n
    
        # Iterate over all pairs (a, b) with a < b
        for a in range(1, n + 1):
            for b in range(a + 1, min(a + t + 1, n + 1) if t else n + 1):
                # With probability p, add an edge from a to b
                if random.random() < p:
                    # Assign a weight to the edge using the specified weight distribution
                    weight = weight_dist()
                    dag.add_edge(a, b, weight=weight)
    
        yield dag
