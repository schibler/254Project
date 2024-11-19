import networkx as nx

class scheduling_alg:

    @classmethod
    def schedule(cls, dag: nx.DiGraph, num_processors: int) -> dict[int, int]:
        raise NotImplemented()

