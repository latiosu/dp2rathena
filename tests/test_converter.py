import importlib
import json
import os

import pytest
import yaml

from dp2rathena import converter


api_key = os.getenv('DIVINEPRIDE_API_KEY')


@pytest.mark.api
def test_fetch_item(fixture):
    convert = converter.Converter(api_key)
    expected_json = json.loads(open(fixture('item_1101.json')).read())
    fetched_json = convert.fetch_item(1101)
    assert fetched_json == expected_json
    assert convert.fetch_item(-1) == {'Id': -1, 'Error': 'Item not found'}
    convert = converter.Converter('fake-api-key')
    with pytest.raises(IOError):
        convert.fetch_item(1101)


def test_wrap_result(fixture):
    convert = converter.Converter(api_key)
    yml = "{ 'Header': { 'Type': 'ITEM_DB', 'Version': 1, }, 'Body': [], }"
    expected_yml = yaml.load(yml, Loader=yaml.FullLoader)
    assert convert.wrap_result([]) == expected_yml
    yml = "{ 'Header': { 'Type': 'ITEM_DB', 'Version': 1, }, 'Body': [{'Key': 'Value'}], }"
    expected_yml = yaml.load(yml, Loader=yaml.FullLoader)
    assert convert.wrap_result([{'Key': 'Value'}]) == expected_yml


@pytest.mark.api
def test_convert(fixture):
    convert = converter.Converter(api_key)
    expected_yml = open(fixture('item_1101_nowrap.yml')).read()
    generated_yml = convert.convert([1101], sort=False, wrap=False)
    assert generated_yml == expected_yml
    expected_yml = open(fixture('item_501_1101_nowrap.yml')).read()
    generated_yml = convert.convert([1101, 501], sort=True, wrap=False)
    assert generated_yml == expected_yml
    expected_yml = open(fixture('item_501_1101.yml')).read()
    generated_yml = convert.convert([501, 1101], sort=False, wrap=True)
    assert generated_yml == expected_yml
    generated_yml = convert.convert([1101, 501], sort=True, wrap=True)
    assert generated_yml == expected_yml


def test_convert_nonapi():
    convert = converter.Converter(api_key)
    generated_yml = convert.convert([], sort=False, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert([], sort=True, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert([], sort=False, wrap=True)
    assert generated_yml == 'Header:\n  Type: ITEM_DB\n  Version: 1\nBody: []\n'
    generated_yml = convert.convert([], sort=True, wrap=True)
    assert generated_yml == 'Header:\n  Type: ITEM_DB\n  Version: 1\nBody: []\n'
