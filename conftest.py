import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--api", action="store_true", default=False, help="run api tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "api: mark test as using api")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--api"):
        # --api given in cli: do not skip api tests
        return
    skip_api = pytest.mark.skip(reason="need --api option to run")
    for item in items:
        if "api" in item.keywords:
            item.add_marker(skip_api)