from typing import List

import networkx as nx
import pytest
from pytest import Config, Item, Session

from .topo import create_graph, mark_as_failure, order_by_dependency, should_skip


@pytest.hookimpl
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    order_by_dependency(items)

    # Group tests for parallel execution
    try:
        config.getvalue("loadgroup")
    except ValueError:
        return

    graph = create_graph(items)
    groups = list(nx.weakly_connected_components(graph))
    for item in items:
        for i, group in enumerate(groups):
            if item.nodeid in group:
                item.add_marker(pytest.mark.xdist_group(str(i)))
                break


@pytest.hookimpl
def pytest_runtest_protocol(item: Item, nextitem: Item):
    if should_skip(item):
        mark_as_failure(item)
        item.add_marker(pytest.mark.skip())


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: Item):
    output = yield
    if output is not None and output.exception:
        mark_as_failure(item)
