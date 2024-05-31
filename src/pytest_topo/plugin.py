from typing import List

import pytest
from pytest import Config, Item, Session

from .topo import mark_as_failure, order_by_dependency, should_skip


@pytest.hookimpl
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]):
    order_by_dependency(items)


@pytest.hookimpl
def pytest_runtest_protocol(item: Item, nextitem: Item):
    if should_skip(item):
        mark_as_failure(item)
        item.add_marker(pytest.mark.skip(), append=False)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: Item):
    output = yield
    if output is not None and output.exception:
        mark_as_failure(item)
