from .conftest import is_hook_called


def test_pytest_collection_modifyitems_is_extendable():
    assert is_hook_called("pytest_collection_modifyitems")


def test_pytest_runtest_protocol_is_extendable():
    assert is_hook_called("pytest_runtest_protocol")


def test_pytest_runtest_call_is_extendable():
    assert is_hook_called("pytest_runtest_call")
