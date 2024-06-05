import pytest

counter = 0


@pytest.mark.dependency("One")
def test_one():
    global counter
    counter += 1
    assert counter == 1


@pytest.mark.depends_on("Two")
def test_three():
    global counter
    counter += 1
    assert counter == 3


@pytest.mark.depends_on("One")
@pytest.mark.dependency("Two")
def test_two():
    global counter
    counter += 1
    assert counter == 2
