import networkx as nx
import sys

def load_dot_graph(file_path):
    """
    Load a directed weighted graph from a .dot file using networkx.
    
    Parameters:
        file_path (str): The path to the .dot file.
    
    Returns:
        nx.DiGraph: A directed weighted graph.
    """
    try:
        # Read the .dot file and create a graph
        graph = nx.DiGraph(nx.drawing.nx_pydot.read_dot(file_path))
        
        # Ensure weights are converted to numeric values
        for u, v, data in graph.edges(data=True):
            if 'weight' in data:
                try:
                    data['weight'] = float(data['weight'])
                except ValueError:
                    print(f"Edge ({u}, {v}) has a non-numeric weight: {data['weight']}. Skipping conversion.")
        
        return graph
    except Exception as e:
        print(f"Error loading graph: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    file_path = sys.argv[1]
    graph = load_dot_graph(file_path)
    
    if graph is not None:
        print("Graph successfully loaded!")
        print(f"Number of nodes: {graph.number_of_nodes()}")
        print(f"Number of edges: {graph.number_of_edges()}")
        
        # Example: print edges with weights
        for u, v, data in graph.edges(data=True):
            print(f"Edge from {u} to {v} with weight {data.get('weight', 'N/A')}")
