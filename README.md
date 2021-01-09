# dp2rathena: Divine-Pride API to rAthena

[![PyPI - Version](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dp2rathena)](https://pypi.org/project/dp2rathena/)
[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)
[![codecov](https://codecov.io/gh/Latiosu/dp2rathena/branch/master/graph/badge.svg?token=B7G9O57UR8)](https://codecov.io/gh/Latiosu/dp2rathena)

Convert Divine-Pride API data to rAthena DB formats (item_db.yml).

## Requirements

* Python 3.6+

## Installation

```
pip install dp2rathena
```

## Usage

A [divine-pride.net](https://www.divine-pride.net/) API key is required, create an account and
generate a key if you don't have one yet.

```bash
dp2rathena config
dp2rathena item 501 1101
```

## Contributing

This project uses [poetry](https://python-poetry.org/) to manage the development enviroment.

* Setup a local development environment with `poetry install`.
* Run tests with `poetry run tox`
* Execute script with `poetry run dp2rathena`

## Changelog

See [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)
