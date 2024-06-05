from typing import Dict, List, Set

import networkx as nx
from pytest import Item


class TopologicalTestSorter:
    func_name_map: Dict[str, str]
    failures: Set[str]
    graph: nx.DiGraph

    def __init__(self, items: List[Item]) -> None:
        self.failures = set()
        self.items = items
        self.func_name_map = self._create_func_name_map()
        self.graph = self._create_graph()
        self.ordered_items = self._order_by_dependency()

    def _create_func_name_map(self) -> Dict[str, str]:
        func_name_map = {}
        for item in self.items:
            mark = item.get_closest_marker("dependency")
            if not mark:
                continue
            for name in mark.args:
                message = f"Duplicate dependency name found: {name}"
                assert name not in func_name_map, message
                func_name_map[name] = item.nodeid
        return func_name_map

    def _create_graph(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        for item in self.items:
            mark = item.get_closest_marker("dependency")
            if mark:
                graph.add_node(item.nodeid)

        for item in self.items:
            mark = item.get_closest_marker("depends_on")
            if mark:
                for name in mark.args:
                    graph.add_edge(self.func_name_map[name], item.nodeid)
        return graph

    def _order_by_dependency(self) -> List[Item]:
        new_order = list(nx.topological_sort(self.graph))
        new_items = []
        for func_name in new_order:
            new_items.extend([item for item in self.items if item.nodeid == func_name])
        return new_items

    def get_ordered_items(self) -> List[Item]:
        return self.ordered_items

    def get_groups(self) -> List[Set[str]]:
        unordered_groups = list(nx.weakly_connected_components(self.graph))
        order = {item.nodeid: i for i, item in enumerate(self.ordered_items)}
        groups = []
        for group in unordered_groups:
            groups.append(sorted(group, key=order.get))
        return groups

    def mark_as_failure(self, item: Item) -> None:
        self.failures.add(item.nodeid)

    def should_skip(self, item: Item) -> bool:
        mark = item.get_closest_marker("depends_on")
        if not mark:
            return False
        for name in mark.args:
            func_name = self.func_name_map[name]
            if func_name in self.failures:
                return True
        return False
