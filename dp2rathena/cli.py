import importlib
import os
import pkg_resources
import re
import sys

import click

from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from dp2rathena import converter


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ENV_PATH = Path('.') / '.env'
CONFIG_PATH = Path.home() / '.dp2rathena.conf'
DP_KEY = 'DIVINEPRIDE_API_KEY'


class ApiKey(click.ParamType):
    name = 'api-key'

    def convert(self, value, param=None, ctx=None):
        if not re.match(r'[0-9a-f]{32}', value):
            self.fail(
                f'{value} is not a 32-character hexadecimal string',
                param,
                ctx,
            )
        return value


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '-k', '--api-key',
    type=ApiKey(),
    help='Divine-Pride API Key.'
)
@click.pass_context
def dp2rathena(ctx, api_key):
    """Converts Divine-Pride API data to rathena DB data.

    \b
    Example:
        dp2rathena config
        dp2rathena item 501
    """
    if ENV_PATH.exists():
        env_values = dotenv_values(dotenv_path=ENV_PATH)
    elif CONFIG_PATH.exists():
        env_values = dotenv_values(dotenv_path=CONFIG_PATH)
    else:
        env_values = dict()

    if api_key:
        ctx.ensure_object(dict)
        ctx.obj[DP_KEY] = api_key
    else:
        ctx.obj = env_values


@dp2rathena.command()
def version():
    """Shows the version of dp2rathena."""
    click.echo(pkg_resources.get_distribution('dp2rathena').version)


@dp2rathena.command()
def config():
    """Configures variables for dp2rathena (api-key)."""
    api_key = input('Enter your Divine-Pride API key: ')
    CONFIG_PATH.write_text(f'{DP_KEY}={api_key}\n')
    click.echo('Configuration saved to ' + str(CONFIG_PATH.resolve()))


@dp2rathena.command()
@click.option(
    '-f', '--file',
    is_flag=True,
    help='A file with item ids to convert, newline separated.'
)
@click.option(
    '--sort/--no-sort',
    default=False,
    help='Sorts result by item id. Default: no sort.'
)
@click.option(
    '--wrap/--no-wrap',
    default=True,
    help='Wraps result with rathena Header and Body tags.'
)
@click.option(
    '--debug',
    is_flag=True,
    help='Shows debug information when querying Divine-Pride.'
)
@click.argument('value', nargs=-1)
@click.pass_context
def item(ctx, file, sort, wrap, debug, value):
    """Converts item ids to rathena item db yaml.

    \b
    Examples:
        # Pass API key and convert item ids 501 and 1101
        dp2rathena --api-key <your-api-key> item 501 1101
    \b
        # Pass API key and convert items via STDIN and sort result by id
        dp2rathena -k <your-api-key> item --sort -f -
    \b
        # Save API key and convert item ids in ids_to_convert.txt
        dp2rathena config
        dp2rathena item -f ids_to_convert.txt
    """
    if file:
        if len(value) != 1:
            raise click.UsageError('One file required for processing.')
        to_convert = click.open_file(value[0], 'r').read().splitlines()
    else:
        if len(value) == 0:
            raise click.UsageError('Item id required.')
        for v in value:
            if not v.isdigit():
                raise click.UsageError(f'Non-integer item id - {v}')
        to_convert = value
    api_key = ctx.obj[DP_KEY]
    click.echo(
        converter.Converter(api_key, debug).convert(to_convert, sort, wrap)
    , nl=False)


if __name__ == '__main__':
    dp2rathena(obj={})