from context import dp2rathena
from dp2rathena import converter

import filecmp
import os
import json

def test_item_schema():
    convert = converter.Converter()
    item_json = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.json').read()
    generated_yml = convert.to_item_yml(json.loads(item_json))
    print(generated_yml)
    expected_yml = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.yml').read()
    assert generated_yml == expected_yml
