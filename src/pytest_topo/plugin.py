from typing import List

import pytest
from pytest import Config, Item, Session

from .topo import TopologicalTestSorter

sorter: TopologicalTestSorter


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    global sorter
    sorter = TopologicalTestSorter(items)
    items[:] = sorter.get_ordered_items()

    # Group tests for parallel execution
    try:
        config.getvalue("loadgroup")
    except ValueError:
        return

    groups = sorter.get_groups()
    for item in items:
        for i, group in enumerate(groups):
            if item.nodeid in group:
                item.add_marker(pytest.mark.xdist_group(str(i)))
                break


@pytest.hookimpl
def pytest_runtest_protocol(item: Item, nextitem: Item):
    if sorter.should_skip(item):
        sorter.mark_as_failure(item)
        item.add_marker(pytest.mark.skip())


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: Item):
    output = yield
    if output is not None and output.exception:
        sorter.mark_as_failure(item)
