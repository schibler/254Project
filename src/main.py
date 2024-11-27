import heapq
import random

import matplotlib.pyplot as plt
import networkx as nx

from draw_graph import draw_dag_topological
from experiment import experiment, experiment_result
from longest_paths import longest_path_lengths
from random_graph import generate_random_dags 
from scheduling_algs.lrp_scheduling_alg import lrp_scheduling_alg

debug = True
iterations = 1000
ratios = []

# Generate a set of graphs
dags = generate_random_dags(iterations, n=10, p=0.3, t=4)
alg = lrp_scheduling_alg()
num_fus = 1

exp = experiment(dags, alg, num_fus)
result = exp.run()
print(f"max ratio = {result.max_ratio()}")
print(f"min ratio = {result.min_ratio()}")
print(f"median ratio = {result.median_ratio()}")
