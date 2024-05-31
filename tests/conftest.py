import pytest

hooks_called = []


def is_hook_called(hook_name):
    return hook_name in hooks_called


@pytest.hookimpl
def pytest_collection_modifyitems(session, config, items):
    hooks_called.append("pytest_collection_modifyitems")


@pytest.hookimpl
def pytest_runtest_protocol(item, nextitem):
    hooks_called.append("pytest_runtest_protocol")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    hooks_called.append("pytest_runtest_call")
    yield
