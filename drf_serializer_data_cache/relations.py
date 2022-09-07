from collections import deque
from drf_serializer_data_cache.utils import get_relation_fields


class BFPForIndirectRelation:
    # This algorithm is quoted from:
    # https://github.com/shellfly/algs4-py/blob/master/algs4/breadth_first_paths.py
    def __init__(self, s):
        self._marked = set()
        self.edge_to = {}
        self.s = s
        self.bfs(s)

    def bfs(self, s):
        self._marked.add(s)
        queue = deque()
        queue.append(s)
        while queue:
            v = queue.popleft()
            for w, lookups in get_relation_fields(v):
                if w not in self._marked:
                    self.edge_to[w] = v, lookups
                    self._marked.add(w)
                    queue.append(w)

    def has_path_to(self, v):
        return v in self._marked

    def path_to(self, v):
        if not self.has_path_to(v):
            return
        path = deque()
        predicate = deque()
        x = v
        while x is not self.s:
            path.append(x)
            edge_to_res = self.edge_to[x]
            x = edge_to_res[0]
            predicate.append(edge_to_res[1])
        path.append(self.s)
        return path, predicate

    def get_predicate(self, model):
        res = None
        lookups_queue = self.path_to(model)[1]
        for i in lookups_queue:
            res = f'{i}__{res}' if res else f'{i}'
        return res
