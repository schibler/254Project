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
dags = list(generate_random_dags(iterations, n=10, p=0.25, t=4))
alg = lrp_scheduling_alg()
num_fus = [1, 2, 4, 8, 16]
for nfu in num_fus:
    exp = experiment(dags, alg, nfu)
    result = exp.run()
    print(f"")
    print(f"\tmax ratio = {result.max_ratio()}")
    print(f"\tmin ratio = {result.min_ratio()}")
    print(f"\tquartile ratios = {result.quartile_ratios()}")

