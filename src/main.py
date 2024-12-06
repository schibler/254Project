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
n=1000
p=0.01
t=100
dags = list(generate_random_dags(iterations, n, p, t=t))
alg = lrp_scheduling_alg()
num_fus = [1, 2, 4, 8]
labels = num_fus
ratios = []
for nfu in num_fus:
    exp = experiment(dags, alg, nfu)
    result = exp.run()
    ratios.append(result.ratios())
    print(f"")
    print(f"\tmax ratio = {result.max_ratio()}")
    print(f"\tmin ratio = {result.min_ratio()}")
    print(f"\tquartile ratios = {result.quartile_ratios()}")

fig = plt.figure(figsize=(10, 7))

# Position and size of the axes ([x, y, width, height])
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
# Add data
bp = ax.boxplot(ratios)

fs = 18
header_fs = fs + 2
# Add labels, title, and ticks
ax.set_title(f'LRP Scheduling on {n} node graphs with p={p}, t={t}', fontsize=header_fs)
ax.set_ylabel('Ratio of schedule length to sequential lower bound', fontsize=fs)
ax.tick_params(axis='y', labelsize=fs)  # Adjust y-axis tick label size
ax.set_xticks(range(1, len(labels) + 1)) # 1-based label x-axis labelling
ax.set_xticklabels(labels, fontsize=fs) # Assign experiment labels
ax.set_xlabel("Number of Functional Units", fontsize=fs)

plt.show()
