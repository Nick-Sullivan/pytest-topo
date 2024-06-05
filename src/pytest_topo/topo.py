from typing import List

import networkx as nx
from pytest import Item

failures = set()
func_name_map = {}


def order_by_dependency(items: List[Item]) -> None:
    graph = create_graph(items)
    new_order = list(nx.topological_sort(graph))

    new_items = []
    for func_name in new_order:
        new_items.extend([item for item in items if item.nodeid == func_name])

    items[:] = new_items


def create_graph(items: List[Item]) -> nx.DiGraph:
    graph = nx.DiGraph()

    for item in items:
        mark = item.get_closest_marker("dependency")
        if not mark:
            continue
        graph.add_node(item.nodeid)
        for name in mark.args:
            assert name not in func_name_map, f"Duplicate dependency name found: {name}"
            func_name_map[name] = item.nodeid

    for item in items:
        mark = item.get_closest_marker("depends_on")
        if not mark:
            continue
        for name in mark.args:
            graph.add_edge(func_name_map[name], item.nodeid)
    return graph


def mark_as_failure(item: Item) -> None:
    failures.add(item.nodeid)


def should_skip(item: Item) -> bool:
    mark = item.get_closest_marker("depends_on")
    if not mark:
        return False
    for name in mark.args:
        func_name = func_name_map[name]
        if func_name in failures:
            return True
    return False
