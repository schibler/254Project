import networkx as nx

def longest_path_lengths(graph):
    # Initialize the dictionary to store longest path lengths
    longest_paths = {node: 0 for node in graph.nodes}
    
    # List to store nodes in reverse topological order
    topological_order = list(nx.topological_sort(graph))[::-1]

    # Process nodes in reverse topological order
    for node in topological_order:
        # Calculate the longest path from the current node to any of its out neighbors
        max_path_length = 0
        for successor in graph.successors(node):
            edge_weight = graph[node][successor].get('weight', 1)  # Default weight is 1 if unspecified
            max_path_length = max(max_path_length, edge_weight + longest_paths[successor])

        # Set the longest path length for this node
        longest_paths[node] = max_path_length

    return longest_paths

def test_longest_paths():
    pass
