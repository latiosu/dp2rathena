import importlib
import os
import pkg_resources
import sys

import click

from dotenv import load_dotenv
from dp2rathena import converter

@click.group()
def dp2rathena():
    """Convert divine-pride api data to rathena db data."""
    load_dotenv()


@dp2rathena.command()
def version():
    """Shows the version of dp2rathena."""
    click.echo(pkg_resources.get_distribution('dp2rathena').version)


@dp2rathena.command()
@click.option('-k', '--api-key', required=True, type=str, envvar='DIVINEPRIDE_API_KEY', help='Divine-Pride API Key.')
@click.option('-i', '--id', 'id_', multiple=True, type=int, help='Item id to convert, multiple allowed.')
@click.option('-f', '--file', type=click.File('r'), help='A file with item ids to convert, newline separated.')
@click.option('--sort/--no-sort', default=False, help='Sorts results by item id. Default: no sort.')
@click.option('--wrap/--no-wrap', default=True, help='Wraps results with rathena Header and Body tags. Default: wrap.')
@click.option('--debug/--no-debug', default=False, help='Shows debug information when querying Divine-Pride.')
def item(api_key, id_, file, sort, wrap, debug):
    """Converts item ids to rathena item db yaml.

    \b
    Examples:
        dp2rathena item --api-key <your-api-key> -i 501 -i 1101
        dp2rathena item -k <your-api-key> -f ids_to_convert.txt
        dp2rathena item -k <your-api-key> --sort -f -
    """
    if id_ and file:
        raise click.UsageError('Both --id and --file were passed, please specify only one.')
    elif id_:
        to_convert = id_
    elif file:
        to_convert = file.read().splitlines()
    else:
        raise click.UsageError('Either --id or --file is required, please specify an option.')

    os.environ['DIVINEPRIDE_API_KEY'] = api_key
    click.echo(converter.Converter(debug).convert(to_convert, sort, wrap), nl=False)


if __name__ == '__main__':
    dp2rathena()