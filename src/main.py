import heapq
import random

import matplotlib.pyplot as plt
import networkx as nx

from draw_graph import draw_dag_topological
from longest_paths import longest_path_lengths
from random_graph import generate_random_dags 
from scheduling_algs.lrp_scheduling_alg import lrp_scheduling_alg

debug = True
iterations = 1
ratios = []

# Generate a set of graphs
dags = generate_random_dags(iterations, n=10, p=0.3, t=4)

for dag in dags:
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

    alg = lrp_scheduling_alg()
    schedule = alg.schedule(dag, 1)
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
