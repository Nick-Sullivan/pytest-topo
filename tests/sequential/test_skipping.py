import pytest


@pytest.mark.dependency("DoesntPass")
def test_deliberate_skip():
    pytest.skip("Deliberate skip")


@pytest.fixture(scope="function")
def bad_fixture():
    raise Exception("This should not have been created")


@pytest.mark.depends_on("DoesntPass")
def test_skip_due_to_dependency(bad_fixture):
    raise Exception("This should have been skipped")
