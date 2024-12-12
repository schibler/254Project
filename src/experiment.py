import matplotlib.pyplot as plt
import networkx as nx

from draw_graph import draw_dag_topological
from longest_paths import longest_path_lengths
from scheduling_algs.scheduling_alg import scheduling_alg

import logging
logger = logging.getLogger(__name__)

class experiment_result:
    def __init__(self, input_graphs: list[nx.DiGraph], schedules: list[dict[int, int]], lower_bounds: list[int]):
        self._dags = input_graphs
        self._schedules = schedules
        self._lower_bounds = lower_bounds
        
    def ratios(self):
        return [max(s.keys()) / float(l) for s, l in zip(self._schedules, self._lower_bounds)]

    def max_ratio(self):
        return max(self.ratios())

    def min_ratio(self):
        return min(self.ratios())

    def _percentile_ratio(self, k: float):
        if k <= 0 or k >= 1:
            raise ValueError(f"Expected k to be percentile strictly between 0 and 1, not {k}")
        return sorted(self.ratios())[int(len(self._schedules) * k)]
    
    def median_ratio(self):
        return self._percentile_ratio(0.5)

    def quartile_ratios(self):
        return {k : self._percentile_ratio(k) for k in (0.25, 0.5, 0.75)}
            
    
class experiment:

    def __init__(self, input_graphs: list[nx.DiGraph], alg: scheduling_alg, fu_counts: dict[int, int]):
        self._input_graphs = input_graphs
        self._alg = alg
        self._fu_counts = fu_counts

    
    def run(self) -> experiment_result:
        lbs = []
        schedules = []
        for dag in self._input_graphs:
            # Compute longest path from each node
            lengths = longest_path_lengths(dag)
            
            # Easy lower bounds:
            #     n: need to schedule every graph node
            #     longest path: need to respect latency precedence constraints
            # Take max of the two
            length_lower_bound = max([lengths[key] for key in lengths])
            lower_bound = max(length_lower_bound, dag.number_of_nodes())

            schedule = self._alg.schedule(dag=dag, fu_counts=self._fu_counts)
            schedules.append(schedule)
            lbs.append(lower_bound)

        return experiment_result(self._input_graphs, schedules, lbs)
