import heapq

import networkx as nx

from longest_paths import longest_path_lengths

class lrp_scheduling_alg:

    def schedule(self, dag: nx.DiGraph, fu_counts: dict[int: int]) -> dict[int, int]:
        # TODO: leverage num_fus
        lengths = longest_path_lengths(dag)
        priority_list = sorted(lengths.keys(), key=lambda k: lengths[k])
        t = 0
        nodes = dag.nodes
        remaining_degree = {}
        ready_queues = {color: [] for color in fu_counts.keys()}
        for n in nodes:
            remaining_degree[n] = 0
    
        for edge in dag.edges:
            remaining_degree[edge[1]] += 1
        for n in nodes:
            if remaining_degree[n] == 0:
                color = dag.nodes[n]['color']
                ready = ready_queues[color]
                heapq.heappush(ready, (0, n))
        ret_schedule = {}
        event_queue = [(0, None)]
        num_scheduled = 0
        while num_scheduled < len(nodes):
            event = heapq.heappop(event_queue)
            t, n = event
            # Time step
            if n is None:
                for color in fu_counts:
                    # Get the corresponding ready queue
                    ready = ready_queues[color]
                    # Pop up to the number of functional units of this color
                    for _ in range(fu_counts[color]):
                        if len(ready) > 0:
                            next_node = heapq.heappop(ready)[1]
                            ret_schedule[t] = next_node
                            num_scheduled += 1
                            # Add dependency resolved events for each edge of the scheduled node
                            for edge in dag.out_edges(next_node, data=True):
                                # Edge from a to b is in form (a, b, {'weight': w})
                                b = edge[1]
                                w = edge[2]['weight']
                                heapq.heappush(event_queue, (t + w - 0.5, b))
                heapq.heappush(event_queue, (t+1, None))
            # Dependency resolved for node n
            else:
                remaining_degree[n] -= 1
                if remaining_degree[n] == 0:
                    ready = ready_queues[dag.nodes[n]['color']]
                    heapq.heappush(ready, (-1 * lengths[n], n))
        return ret_schedule
