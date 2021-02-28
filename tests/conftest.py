import json

import pytest


@pytest.fixture(scope='session')
def order():
    with open('tests/fixtures/order.json', 'r') as f:
        return json.loads(f.read())


@pytest.fixture(scope='session')
def extracted_from_order():
    with open('tests/fixtures/extracted_from_order.json', 'r') as f:
        return json.loads(f.read())
