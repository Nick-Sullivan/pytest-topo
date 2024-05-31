from pytest_topo.main import hello


def test_hello():
    assert hello("world") == "Hello, world!"
