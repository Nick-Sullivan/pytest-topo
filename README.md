## Install

```bash
pip install pytest-topo
```
The pytest-topo library offers a topological ordering feature for pytest tests, ensuring that dependent tests are run in the correct sequence. This is particularly useful for integration testing libraries that use pytest for orchestration. 

Please note that this library is not recommended for unit tests, as unit tests should ideally be independent of each other.

## Usage Examples

To sequence your tests, apply the `dependency` and `depends_on` markers.

```python
import pytest

@pytest.mark.dependency("One")
def test_one():
    # This test is executed first

@pytest.mark.depends_on("Two")
def test_three():
    # This test is executed third

@pytest.mark.depends_on("One")
@pytest.mark.dependency("Two")
def test_two():
    # This test is executed second
```

If any of the dependent tests do not pass, they will not be skipped. This will also skip any fixture creation, if there are no remaining tests that need to use them.

```python
import pytest

@pytest.mark.dependency("DoesntPass")
def test_one():
    assert False  # force a failure

@pytest.fixture(scope="function")
def my_fixture():
    # This fixture is never created

@pytest.mark.depends_on("DoesntPass")
def test_two(my_fixture):
    # This test will be skipped

```

## Motivation

Consider software where customers register with an `account` API, and submit purchases to a `purchases` API. These are two services with API tests that could look like this:

```
tests
  - account
    - test_create_and_delete
    - ...
  - purchases
    - test_make_purchase
    - ...
```

The `purchases` tests may run a pre-test setup to create an account, execute tests, then run a post-test teardown. If there is an issue in the account creation or deletion, all these tests will error. By adding dependencies, the `purchases` tests will be skipped, reducing test failure noise.
