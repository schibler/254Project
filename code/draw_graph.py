import networkx as nx
import matplotlib.pyplot as plt

def draw_dag_topological(graph):
    # Perform a topological sort to get the node order
    topo_order = list(nx.topological_sort(graph))
    
    # Create a dictionary for positions, where each layer is assigned an x position
    pos = {}
    layer = 0
    
    for i, node in enumerate(topo_order):
        pos[node] = (layer, -i)  # x = layer, y = -i for vertical separation
        # Check if current node has any outgoing edges; if not, increment the layer
        if not list(graph.successors(node)):
            layer += 1
    
    # Draw the graph in the specified position layout
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
    
    # Draw edge weights if they exist
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    plt.title("DAG in Rough Topological Order")
    plt.show()

# Example usage
if __name__ == '__main__':
    G = nx.DiGraph()
    G.add_edge(1, 2, weight=4)
    G.add_edge(1, 3, weight=2)
    G.add_edge(2, 4, weight=7)
    G.add_edge(3, 4, weight=1)
    G.add_edge(1, 5, weight=3)
    G.add_edge(5, 6, weight=1)
    
    draw_dag_topological(G)
