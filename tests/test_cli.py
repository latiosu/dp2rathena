import os
import re

import pytest

from click.testing import CliRunner
from dp2rathena import cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena, ['version'])
    assert not result.exception
    assert re.fullmatch(r'\d+\.\d+\.\d+', result.output.rstrip())


def test_config():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli.dp2rathena, ['config'], input="abc-123")
        assert not result.exception
        assert 'Enter your Divine-Pride API key:' in result.output
        assert 'Configuration saved to' in result.output
        result = runner.invoke(cli.dp2rathena, ['config'], input="aaaabbbbccccdddd1111222233334444")
        assert not result.exception
        assert 'Enter your Divine-Pride API key:' in result.output
        assert 'Configuration saved to' in result.output


@pytest.mark.api
def test_item_invalid(fixture):
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena, ['item'])
    assert result.exit_code == 2
    assert 'Item id required' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', 'hello'])
    assert result.exit_code == 2
    assert 'Non-integer item id' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', 'hello', 'world'])
    assert result.exit_code == 2
    assert 'Non-integer item id' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-f'])
    assert result.exit_code == 2
    assert 'One file required for processing' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-f', 'missing.txt'])
    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)
    result = runner.invoke(cli.dp2rathena, ['item', '123', '-f', fixture('1101_501.txt')])
    assert result.exit_code == 2
    assert 'One file required for processing' in result.output


@pytest.mark.api
def test_item_valid(fixture):
    runner = CliRunner()
    with open(fixture('item_501.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '501'])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-f', '-'], input='501')
        assert result.exit_code == 0
        assert result.output == expected
    with open(fixture('item_501_1101.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '501', '1101'])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '--sort', '1101', '501'])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-f', fixture('1101_501.txt'), '--sort'])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-f', '-', '--sort'], input='1101\n501')
        assert result.exit_code == 0
        assert result.output == expected
    with open(fixture('item_1101_501.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '-f', fixture('1101_501.txt')])
        assert result.exit_code == 0
        assert result.output == expected
    with open(fixture('item_900_1101.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '900', '1101', '--sort'])
        assert result.exit_code == 0
        assert result.output == expected
