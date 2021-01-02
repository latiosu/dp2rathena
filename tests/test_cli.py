import os
import pytest
import re

from click.testing import CliRunner
from dp2rathena import cli


def fixture(filename):
    current_path = os.path.join(os.getcwd(), os.path.dirname(__file__))
    return os.path.join(os.path.realpath(current_path), 'fixtures', filename)


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena, ['version'])
    assert not result.exception
    assert re.fullmatch(r'\d+\.\d+\.\d+', result.output.rstrip())


def test_item_invalid():
    runner = CliRunner()
    result = runner.invoke(cli.dp2rathena, ['item'])
    assert result.exit_code == 2
    assert 'Either --id or --file is required' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k'])
    assert result.exit_code == 2
    assert 'Error: -k option requires an argument' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 123])
    assert result.exit_code == 2
    assert 'Either --id or --file is required' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 'key', '-i'])
    assert result.exit_code == 2
    assert 'Error: -i option requires an argument' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 'key', '-i', 'hello'])
    assert result.exit_code == 2
    assert 'not a valid integer' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 'key', '-f'])
    assert result.exit_code == 2
    assert 'Error: -f option requires an argument' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 'key', '-f', 'missing.txt'])
    assert result.exit_code == 2
    assert 'Could not open file: missing.txt: No such file' in result.output
    result = runner.invoke(cli.dp2rathena, ['item', '-k', 'key', '-i', 123, '-f', fixture('1101_501.txt')])
    assert result.exit_code == 2
    assert 'Error: Both --id and --file were passed' in result.output


@pytest.mark.api
def test_item_success():
    # Note: These tests rely on API key being set in .env
    runner = CliRunner()
    with open(fixture('item_501.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '-i', 501])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-i', '501'])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-f', '-'], input='501')
        assert result.exit_code == 0
        assert result.output == expected
    with open(fixture('item_501_1101.yml')) as f:
        expected = f.read()
        result = runner.invoke(cli.dp2rathena, ['item', '-i', 501, '-i', 1101])
        assert result.exit_code == 0
        assert result.output == expected
        result = runner.invoke(cli.dp2rathena, ['item', '-i', 1101, '-i', 501, '--sort'])
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
