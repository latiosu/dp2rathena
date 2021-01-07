# dp2rathena: Divine-Pride API to rAthena

[![PyPI](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)
[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)

Convert Divine-Pride API data to rAthena DB formats (item_db.yml).

## Requirements

* Python 3.7+

## Installation

```
pip install dp2rathena
```

## Usage

Generate a [divine-pride.net](https://www.divine-pride.net/) API key if you don't have one yet.

```bash
# Fetch items with id 501 and 1101
dp2rathena item --api-key <your-api-key> -i 501 -i 1101
```

Alternatively, you can use an environment variable to pass your API key:
```bash
export DIVINEPRIDE_API_KEY=<your-api-key>
dp2rathena item -i 501 -i 1101
```

## Contributing

This project uses [poetry](https://python-poetry.org/) to manage the development enviroment.

* Setup a local development environment with `poetry install`.
* Run tests with `poetry run pytest`
* Execute script with `poetry run dp2rathena`

## Changelog

See [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)
