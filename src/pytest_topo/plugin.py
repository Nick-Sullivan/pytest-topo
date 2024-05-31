import pytest

from .topo import mark_as_failure, order_by_dependency, should_skip


@pytest.hookimpl
def pytest_collection_modifyitems(session, config, items):
    order_by_dependency(items)


@pytest.hookimpl
def pytest_runtest_protocol(item, nextitem):
    if should_skip(item):
        mark_as_failure(item)
        pytest.skip("Skipped due to dependency failure")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    output = yield
    if output is not None and output.exception:
        mark_as_failure(item)
