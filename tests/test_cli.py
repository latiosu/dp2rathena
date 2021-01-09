import os
import re

import pytest

from pathlib import Path
from click.testing import CliRunner
from dp2rathena import cli


def test_dp2rathena():
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena)
    assert not result.exception
    assert 'Converts Divine-Pride API data to rathena DB data' in result.output
    result = runner.invoke(cli.dp2rathena, ['--api-key'])
    assert result.exception
    assert 'Error: --api-key option requires an argument' in result.output
    result = runner.invoke(cli.dp2rathena, ['--api-key', 'hello'])
    assert result.exception
    assert 'is not a 32-character hexadecimal string' in result.output
    result = runner.invoke(cli.dp2rathena, ['--api-key', '12345678aaaabbbb00000000ffffffff'])
    assert result.exception
    assert 'Missing command' in result.output
    with runner.isolated_filesystem():
        env_path = Path('.') / '.env'
        env_path.write_text('DIVINEPRIDE_API_KEY=abc123\n')
        result = runner.invoke(cli.dp2rathena)
        assert not result.exception
        assert 'Converts Divine-Pride API data to rathena DB data' in result.output
    with runner.isolated_filesystem():
        config_path = Path.home() / '.dp2rathena.conf'
        config_path.write_text('DIVINEPRIDE_API_KEY=abc123\n')
        result = runner.invoke(cli.dp2rathena)
        assert not result.exception
        assert 'Converts Divine-Pride API data to rathena DB data' in result.output


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena, ['version'])
    assert not result.exception
    assert re.fullmatch(r'\d+\.\d+\.\d+', result.output.rstrip())


def test_config():
    runner = CliRunner()
    config_path = Path.home() / '.dp2rathena.conf'
    with runner.isolated_filesystem():
        result = runner.invoke(cli.dp2rathena, ['config'], input="abc-123")
        assert not result.exception
        assert 'Enter your Divine-Pride API key:' in result.output
        assert 'Configuration saved to' in result.output
        assert config_path.exists()
        result = runner.invoke(cli.dp2rathena, ['config'], input="aaaabbbbccccdddd1111222233334444")
        assert not result.exception
        assert 'Enter your Divine-Pride API key:' in result.output
        assert 'Configuration saved to' in result.output
        assert config_path.exists()


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
    result = runner.invoke(cli.dp2rathena, ['-k', 'aaaabbbbccccdddd1111222233334444', 'item', '501'])
    assert result.exit_code == 1
    assert isinstance(result.exception, IOError)
