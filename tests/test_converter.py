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
    expected_json = json.loads(open(fixture('item_1101.json'), encoding='utf-8').read())
    fetched_json = convert.fetch_item(1101)
    assert fetched_json == expected_json
    assert convert.fetch_item(-1) == {'Id': -1, 'Error': 'Item not found'}
    convert = converter.Converter('fake-api-key')
    with pytest.raises(IOError):
        convert.fetch_item(1101)


@pytest.mark.api
def test_fetch_mob(fixture):
    convert = converter.Converter(api_key)
    expected_json = json.loads(open(fixture('mob_1002.json'), encoding='utf-8').read())
    fetched_json = convert.fetch_mob(1002)
    assert fetched_json == expected_json
    assert convert.fetch_mob(-1) == 'Id: -1, Error: Mob not found'
    convert = converter.Converter('fake-api-key')
    with pytest.raises(IOError):
        convert.fetch_mob(1002)


@pytest.mark.api
def test_convert_item(fixture):
    convert = converter.Converter(api_key)
    expected_yml = open(fixture('item_1101_nowrap.yml'), encoding='utf-8').read()
    generated_yml = convert.convert_item([1101], sort=False, wrap=False)
    assert generated_yml == expected_yml
    expected_yml = open(fixture('item_501_1101_nowrap.yml'), encoding='utf-8').read()
    generated_yml = convert.convert_item([1101, 501], sort=True, wrap=False)
    assert generated_yml == expected_yml
    expected_yml = open(fixture('item_501_1101.yml'), encoding='utf-8').read()
    generated_yml = convert.convert_item([501, 1101], sort=False, wrap=True)
    assert generated_yml == expected_yml
    generated_yml = convert.convert_item([1101, 501], sort=True, wrap=True)
    assert generated_yml == expected_yml
    generated_yml = convert.convert_item([501, '', 1101], sort=False, wrap=True)
    assert generated_yml == expected_yml


def test_convert_item_nonapi():
    convert = converter.Converter(api_key)
    generated_yml = convert.convert_item([], sort=False, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert_item([], sort=True, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert_item([], sort=False, wrap=True)
    assert generated_yml == 'Header:\n  Type: ITEM_DB\n  Version: 1\nBody: []\n'
    generated_yml = convert.convert_item([], sort=True, wrap=True)
    assert generated_yml == 'Header:\n  Type: ITEM_DB\n  Version: 1\nBody: []\n'


@pytest.mark.api
def test_convert_mob_skill(fixture):
    convert = converter.Converter(api_key)
    expected = open(fixture('mob_skill_1002.txt'), encoding='utf-8').read()
    generated = convert.convert_mob_skill([1002])
    assert generated == expected
    expected = open(fixture('mob_skill_1002_1049.txt'), encoding='utf-8').read()
    generated = convert.convert_mob_skill([1002, 1049])
    assert generated == expected
    generated = convert.convert_mob_skill([1002, '', 1049])
    assert generated == expected
    expected = open(fixture('mob_skill_1049_1002.txt'), encoding='utf-8').read()
    generated = convert.convert_mob_skill([1049, 1002])
    assert generated == expected


def test_convert_mob_skill_nonapi():
    convert = converter.Converter(api_key)
    generated_txt = convert.convert_mob_skill([])
    assert generated_txt == ''
    generated_txt = convert.convert_mob_skill([''])
    assert generated_txt == ''


@pytest.mark.api
def test_convert_mob(fixture):
    convert = converter.Converter(api_key)
    expected = open(fixture('mob_1002.yml'), encoding='utf-8').read()
    generated = convert.convert_mob([1002])
    assert generated == expected
    expected = open(fixture('mob_1002_1049.yml'), encoding='utf-8').read()
    generated = convert.convert_mob([1002, 1049])
    assert generated == expected
    generated = convert.convert_mob([1002, '', 1049])
    assert generated == expected
    expected = open(fixture('mob_1049_1002.yml'), encoding='utf-8').read()
    generated = convert.convert_mob([1049, 1002])
    assert generated == expected


def test_convert_mob_nonapi():
    convert = converter.Converter(api_key)
    generated_yml = convert.convert_mob([], sort=False, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert_mob([], sort=True, wrap=False)
    assert generated_yml == '[]\n'
    generated_yml = convert.convert_mob([], sort=False, wrap=True)
    assert generated_yml == 'Header:\n  Type: MOB_DB\n  Version: 2\nBody: []\n'
    generated_yml = convert.convert_mob([], sort=True, wrap=True)
    assert generated_yml == 'Header:\n  Type: MOB_DB\n  Version: 2\nBody: []\n'


def test_remove_numerical_quotes():
    convert = converter.Converter(api_key)
    result = convert.remove_numerical_quotes('\'01\'')
    assert result == '01'
    result = convert.remove_numerical_quotes('Tell\'tale')
    assert result == 'Tell\'tale'