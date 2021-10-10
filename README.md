<h1 align="center">
  dp2rathena
</h1>

<p align="center">
  <a href="https://pypi.org/project/dp2rathena/">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/dp2rathena">
  </a>
  <a href="https://pypi.org/project/dp2rathena/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dp2rathena">
  </a>
  <a href="https://travis-ci.com/github/latiosu/dp2rathena">
    <img alt="TravisCI Status" src="https://img.shields.io/travis/com/latiosu/dp2rathena">
  </a>
  <a href="https://codecov.io/gh/latiosu/dp2rathena">
    <img alt="codecov" src="https://codecov.io/gh/latiosu/dp2rathena/branch/master/graph/badge.svg?token=B7G9O57UR8"/>
  </a>
</p>

<h3 align="center">
  Convert Divine-Pride API data to rAthena text database formats
</h3>

<p align="center">
  dp2rathena is an open-source command-line tool, helping developers save time updating their rAthena database data.
</p>

<p align="center">
  <img alt="dp2rathena terminal animation" src="https://user-images.githubusercontent.com/7020503/136682386-f920f53e-cadc-4feb-891b-95a86fcbf95c.gif">
</p>


<br />

## ✨ Features

- `item_db.yml`
- `mob_db.yml`
- `mob_skill_db.txt`
- `mob_db.txt` (planned)
- `skill_db.yml` (planned)

## 🏁 Getting Started

**Requirements**

* [Python 3.6+](https://www.python.org/downloads/)

**Installation**

```
pip install dp2rathena
```

## 💻 Usage

A [divine-pride.net](https://www.divine-pride.net/) API key is required, create an account and generate a key if you don't have one yet.

```bash
# Store API key
dp2rathena config

# Convert items with ids 501 and 1101
dp2rathena item 501 1101

# Convert mob with id 20355
dp2rathena mob 20355

# Convert mob skills from mob ids in a newline separated file
dp2rathena mobskill -f my_mobs.txt

# Print out help text
dp2rathena -h
```

## 🛠️ Limitations

All fields are mapped except the ones listed below:

### `item_db.yml`

**Partially Mapped**
- `"Type"` - when the item type is "Consumable" on DP and subtype "Special", we output a few possible options for user to choose the correct one (Healing, Usable, DelayConsume or Cash)
- `"SubType"` - when the item type is "Ammo" on DP, we output all rathena ammo subtypes for user to choose correct option as DP doesn't map all rathena ammo subtypes

**Not Mapped** _(insufficient data)_
- `"Script"` / `"EquipScript"` / `"UnEquipScript"` - script to execute when some action is performed with the item
- `"Class"` - upper class types that can equip item
- `"Flags"` - item flags such as `"BuyingStore"`, `"DeadBranch"`, `"BindOnEquip"`, etc...
- `"Delay"` - item use delay
- `"Stack"` - item stack amount
- `"NoUse"` - conditions when the item is unusable
- `"AliasName"` - another item's AegisName to be sent to client instead of this AegisName

### `mob_db.yml`

**Not Mapped** _(insufficient data)_
- `MvpExp` - MVP experience gained
- `RaceGroups` - list of secondary groups the monster may be part of
- `Modes` - list of unique behavior not defined by AI, Class, or Attribute
- `JapaneseName` - name in Japanese
- `Drops > RandomOptionGroup` - the Random Option Group applied to item on drop
- `Drops > Index` - index used for overwriting item

**Notes**
- `Ai` - not always defined on DP and needs manual input (refer to [rathena docs](https://github.com/rathena/rathena/blob/master/doc/mob_db_mode_list.txt))
- `Drops > Item` - relies on an internal db yaml file (updated every dp2rathena release) to determine output aegis name

## 🙌 Contributing

This project uses [poetry](https://python-poetry.org/) to manage the development environment.

* Setup a local development environment with `poetry install`
* Run tests with `poetry run tox` (or `pytest` for current python version)
* Run live API tests with `poetry run pytest --api`
* Update internal db yamls with `poetry run python tools/generate_item_db.py` (or `tools/generate_skill_db.py`)
* Execute script with `poetry run dp2rathena`

## 📰 Changelog

See [CHANGELOG.md](https://github.com/latiosu/dp2rathena/blob/master/CHANGELOG.md)

## 📝 License

See [LICENSE](https://github.com/latiosu/dp2rathena/blob/master/LICENSE)
