import heapq

import networkx as nx

from longest_paths import longest_path_lengths

class lrp_scheduling_alg:

    @classmethod
    def schedule(cls, dag: nx.DiGraph, num_processors: int) -> dict[int, int]:
        # TODO: leverage num_processors
        lengths = longest_path_lengths(dag)
        priority_list = sorted(lengths.keys(), key=lambda k: lengths[k])
        t = 0
        nodes = dag.nodes
        remaining_degree = {}
        not_ready = set()
        ready = []
        for n in nodes:
            remaining_degree[n] = 0
    
        for edge in dag.edges:
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
                    not_ready.remove(n)
                    heapq.heappush(ready, (-1 * lengths[n], n))
        return schedule