import time

import pytest

counter_b = 0
start_time = time.time()
delay = 1


@pytest.mark.dependency("A-1")
def test_a_one():
    time.sleep(delay)


@pytest.mark.depends_on("A-1")
def test_a_two():
    duration = time.time() - start_time
    assert duration < 2 * delay


@pytest.mark.dependency("B-1")
def test_b_one():
    time.sleep(delay)


@pytest.mark.depends_on("B-1")
def test_b_two():
    duration = time.time() - start_time
    assert duration < 2 * delay
