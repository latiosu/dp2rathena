import filecmp
import importlib
import os

import json
import pytest

from dp2rathena import converter

# TODO: implement remaining item mapper functions
# def test_to_item_yml():
#     convert = converter.Converter()
#     item_json = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.json').read()
#     generated_yml = convert.to_item_yml(json.loads(item_json))
#     expected_yml = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.yml').read()
#     assert generated_yml == expected_yml

@pytest.mark.api
def test_fetch_item_api():
    convert = converter.Converter()
    item_json = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.json').read()
    expected_json = json.loads(item_json)
    fetched_json = convert.fetch_item(1101)
    assert fetched_json == expected_json