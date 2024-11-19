import heapq
import random

import matplotlib.pyplot as plt
import networkx as nx

from draw_graph import draw_dag_topological
from longest_paths import longest_path_lengths
from random_graph import generate_random_dag 

def schedule_lrp(weighted_dag):
    lengths = longest_path_lengths(dag)
    priority_list = sorted(lengths.keys(), key=lambda k: lengths[k])
    t = 0
    nodes = weighted_dag.nodes
    remaining_degree = {}
    not_ready = set()
    ready = []
    for n in nodes:
        remaining_degree[n] = 0

    for edge in weighted_dag.edges:
        remaining_degree[edge[1]] += 1
    for n in nodes:
        if remaining_degree[n] > 0:
            not_ready.add(n)
        else:
            heapq.heappush(ready, (0, n))
    schedule = {}
    event_queue = [(0, None)]
    while len(schedule) < len(nodes):
        event = heapq.heappop(event_queue)
        t, n = event
        # Time step
        if n is None:
            if len(ready) > 0:
                next_node = heapq.heappop(ready)[1]
                schedule[t] = next_node
                for edge in weighted_dag.out_edges(next_node, data=True):
                    # Edge from a to b is in form (a, b, {'weight': w})
                    b = edge[1]
                    w = edge[2]['weight']
                    heapq.heappush(event_queue, (t + w - 0.5, b))
                    
            heapq.heappush(event_queue, (t+1, None))
        # Dependency resolved for node n
        else:
            remaining_degree[n] -= 1
            if remaining_degree[n] == 0:
                not_ready.remove(n)
                heapq.heappush(ready, (-1 * lengths[n], n))
    return schedule



debug = True
iterations = 1
ratios = []

for _ in range(iterations):

    # Custom weight distribution function
    custom_weight_dist = lambda: random.randint(1, 20)
    
    # Generate the graph
    dag = generate_random_dag(n=10, p=0.3, t=4, weight_dist=custom_weight_dist)
    
    # Print the generated edges with weights
    if debug:
        for u, v, weight in dag.edges(data='weight'):
            print(f"Edge from {u} to {v} with weight {weight}")
    
    lengths = longest_path_lengths(dag)
    
    # Easy lower bounds:
    #     n: need to schedule every graph node
    #     longest path: need to respect latency precedence constraints
    # Take max of the two
    length_lower_bound = max([lengths[key] for key in lengths])
    lower_bound = max(length_lower_bound, dag.number_of_nodes())
    
    if debug:
        print(f'lengths: {lengths}')
    
    schedule = schedule_lrp(dag)
    schedule_time = max(schedule.keys())
    ratio = schedule_time / float(lower_bound)
    
    if debug:
        print(f'schedule: {schedule}')
        print(f"schedule time = {schedule_time}")
        print(f"lower bound = {lower_bound}")
        print(f"ratio = {ratio}\n")
        draw_dag_topological(dag)
    ratios.append(ratio)

ratios = sorted(ratios)
print(f"max ratio = {max(ratios)}")
print(f"min ratio = {min(ratios)}")
print(f"median ratio = {ratios[int(len(ratios)/2)]}")
