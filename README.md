# dp2rathena: Divine-Pride API to rAthena

[![PyPI - Version](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dp2rathena)](https://pypi.org/project/dp2rathena/)
[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)
[![codecov](https://codecov.io/gh/Latiosu/dp2rathena/branch/master/graph/badge.svg?token=B7G9O57UR8)](https://codecov.io/gh/Latiosu/dp2rathena)

Convert Divine-Pride API data to rAthena DB formats.

Currently supported formats are:
- item_db.yml
- (coming soon) mob_skill_db.txt

## Requirements

* Python 3.6+

## Installation

```
pip install dp2rathena
```

## Usage

A [divine-pride.net](https://www.divine-pride.net/) API key is required, create an account and generate a key if you don't have one yet.

```bash
dp2rathena config
dp2rathena item 501 1101
```

## Limitations

Currently only items can be converted and with the following limitations:

- `"Type"` - when the item type is "Consumable" on DP and subtype "Special", we output a few possible options for user to choose the correct one (Healing, Usable, DelayConsume or Cash)
- `"SubType"` - when the item type is "Ammo" on DP, we output all rathena ammo subtypes for user to choose correct option as DP doesn't map all rathena ammo subtypes

The following item_db.yml fields are excluded as DP API doesn't expose sufficient data to reverse-engineer the mapping:

- `"Script"` / `"EquipScript"` / `"UnEquipScript"` - script to execute when some action is performed with the item
- `"Class"` - upper class types that can equip item
- `"Flags"` - item flags such as `"BuyingStore"`, `"DeadBranch"`, `"BindOnEquip"`, etc...
- `"Delay"` - item use delay
- `"Stack"` - item stack amount
- `"NoUse"` - conditions when the item is unusable
- `"View"` - view sprite of the item
- `"AliasName"` - another item's AegisName to be sent to client instead of this AegisName

## Contributing

This project uses [poetry](https://python-poetry.org/) to manage the development environment.

* Setup a local development environment with `poetry install`.
* Run tests with `poetry run tox`
* Execute script with `poetry run dp2rathena`

## Changelog

See [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)

## License

See [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)
