import filecmp
import os

import json
import pytest

from context import dp2rathena
from dp2rathena import item_mapper

# TODO: implement remaining item mapper functions
# def test_item_mapper():
#     convert = item_mapper.Mapper()
#     item_json = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.json').read()
#     generated_yml = convert.to_item_yml(json.loads(item_json))
#     print(generated_yml)
#     expected_yml = open(os.path.dirname(os.path.realpath(__file__)) + '/fixtures/item_1101.yml').read()
#     assert generated_yml == expected_yml

def test_mapping_name():
    mapper = item_mapper.Mapper()
    assert mapper.name({'name': None}) == ''
    assert mapper.name({'name': ''}) == ''
    assert mapper.name({'name': '100T Zeny Check'}) == '100T Zeny Check'
    assert mapper.name({'name': 'Knife [4]'}) == 'Knife'
    assert mapper.name({'name': 'Hunting Bow [2]'}) == 'Hunting Bow'
    assert mapper.name({'name': '[Katsua]Adventurer\'s Backpack [1]'}) == '[Katsua]Adventurer\'s Backpack'
    assert mapper.name({'name': 'Travel Brochure [Amatsu]'}) == 'Travel Brochure [Amatsu]'
    assert mapper.name({'name': 'MATK+1%(Lower)'}) == 'MATK+1%(Lower)'


def test_mapping_itemTypeId():
    mapper = item_mapper.Mapper()
    assert mapper.itemTypeId({'itemTypeId': 0, 'itemSubTypeId': 0}) is None
    with pytest.raises(AssertionError):
        mapper.itemTypeId({'itemTypeId': -1, 'itemSubTypeId': -1})
        mapper.itemTypeId({'itemTypeId': 1, 'itemSubTypeId': -1})
    assert mapper.itemTypeId({'itemTypeId': 1, 'itemSubTypeId': 0}) == 'Weapon'
    assert mapper.itemTypeId({'itemTypeId': 2, 'itemSubTypeId': 518, 'name': 'Isis Egg'}) == 'PetEgg'
    assert mapper.itemTypeId({'itemTypeId': 2, 'itemSubTypeId': 518, 'name': 'Broken Shell'}) == 'PetArmor'
    assert mapper.itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 0}) == 'Consumable'
    assert mapper.itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 768}) == 'Healing/Usable/DelayConsume/Cash'
    assert mapper.itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 769}) == 'Healing'
    assert mapper.itemTypeId({'itemTypeId': 9, 'itemSubTypeId': 0}) == 'Armor'
    assert mapper.itemTypeId({'itemTypeId': 10, 'itemSubTypeId': 0}) == 'ShadowGear'


def test_mapping_itemSubTypeId():
    mapper = item_mapper.Mapper()
    assert mapper.itemSubTypeId({'itemTypeId': 0, 'itemSubTypeId': 0}) is None
    with pytest.raises(AssertionError):
        mapper.itemSubTypeId({'itemTypeId': -1, 'itemSubTypeId': -1})
        mapper.itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': -1})
    assert mapper.itemSubTypeId({'itemTypeId': 4, 'itemSubTypeId': 1025}) \
        == 'Arrow/Dagger/Bullet/Shell/Grenade/Shuriken/Kunai/CannonBall/ThrowWeapon'
    assert mapper.itemSubTypeId({'itemTypeId': 4, 'itemSubTypeId': 0}) \
        == 'Arrow/Dagger/Bullet/Shell/Grenade/Shuriken/Kunai/CannonBall/ThrowWeapon'
    assert mapper.itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': 258}) == '2hSword'
    assert mapper.itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': 0}) is None
    assert mapper.itemSubTypeId({'itemTypeId': 2, 'itemSubTypeId': 512}) is None
    assert mapper.itemSubTypeId({'itemTypeId': 10, 'itemSubTypeId': 526}) is None


def test_mapping_sell():
    mapper = item_mapper.Mapper()
    assert mapper.sell({}) is None


def test_mapping_weight():
    mapper = item_mapper.Mapper()
    assert mapper.weight({'weight': 0}) == 0
    assert mapper.weight({'weight': 50.0}) == 500
    assert mapper.weight({'weight': 0.1}) == 1
    assert mapper.weight({'weight': -1}) == 0


def test_mapping_job():
    mapper = item_mapper.Mapper()
    assert mapper.job({'job': None}) is None
    assert mapper.job({'job': 0xFFFFF}) is None
    assert mapper.job({'job': 0}) is None
    with pytest.raises(AssertionError):
        mapper.job({'job': -1})
        mapper.job({'job': 0x100000})
    assert mapper.job({'job': 0x20410}) == {'Acolyte': True, 'Monk': True, 'Priest': True}
    assert mapper.job({'job': 1}) == {'Novice': True, 'SuperNovice': True}
    assert mapper.job({'job': 142}) == {'Summoner': True}
    assert mapper.job({'job': 144}) == {'KagerouOboro': True, 'Rebellion': True}


# TODO ...
# def test_mapping_classNum():
#     mapper = item_mapper.Mapper()
#     assert mapper.classNum({'classNum': 0}) is None
#     assert mapper.classNum({'classNum': -1}) is None
#     assert mapper.classNum({'classNum': 1}) == ''
#     assert mapper.classNum({'classNum': 5}) == ''
#     assert mapper.classNum({'classNum': 10}) == ''

def test_mapping_gender():
    mapper = item_mapper.Mapper()
    assert mapper.gender({'job': None}) is None
    assert mapper.gender({'job': 1}) is None
    assert mapper.gender({'job': 0xFFFFF}) is None
    with pytest.raises(AssertionError):
        mapper.gender({'job': -1})
        mapper.gender({'job': 0x100000})
    assert mapper.gender({'job': 0x08000}) == 'Male'
    assert mapper.gender({'job': 0x10000}) == 'Female'
    assert mapper.gender({'job': 0x18000}) == 'Both'

def test_mapping_locationId():
    mapper = item_mapper.Mapper()
    assert mapper.locationId({'locationId': None, 'itemTypeId': 0}) is None
    assert mapper.locationId({'locationId': 0, 'itemTypeId': 0}) is None
    with pytest.raises(AssertionError):
        mapper.locationId({'locationId': -1, 'itemTypeId': 0})
        mapper.locationId({'locationId': 0x400000, 'itemTypeId': 0})
    assert mapper.locationId({'locationId': 0x10, 'itemTypeId': 0}) == {'Armor': True}
    assert mapper.locationId({'locationId': 0, 'itemTypeId': 4}) == {'Ammo': True}
    assert mapper.locationId({'locationId': 0x22, 'itemTypeId': 0}) == {'Both_Hand': True}
    assert mapper.locationId({'locationId': 0x88, 'itemTypeId': 0}) == {'Both_Accessory': True}
    assert mapper.locationId({'locationId': 0x10000, 'itemTypeId': 0}) == {'Shadow_Armor': True}
    assert mapper.locationId({'locationId': 0x400, 'itemTypeId': 0}) == {'Costume_Head_Top': True}
    assert mapper.locationId({'locationId': 0x300, 'itemTypeId': 0}) \
        == {'Head_Top': True, 'Head_Mid': True}
    assert mapper.locationId({'locationId': 0x301, 'itemTypeId': 0}) \
        == {'Head_Top': True, 'Head_Mid': True, 'Head_Low': True}

def test_mapping_itemLevel():
    mapper = item_mapper.Mapper()
    assert mapper.itemLevel({'itemTypeId': 0}) is None
    with pytest.raises(AssertionError):
        mapper.itemLevel({'itemTypeId': -1})
    assert mapper.itemLevel({'itemTypeId': 1}) == '1/2/3/4'
    assert mapper.itemLevel({'itemTypeId': 2}) is None

def test_mapping_itemMoveInfo():
    mapper = item_mapper.Mapper()
    assert mapper.itemMoveInfo({'itemMoveInfo': {
        'drop': True,
        'trade': True,
        'store': True,
        'cart': True,
        'sell': True,
        'mail': True,
        'auction': True,
        'guildStore': True
    }}) is None
    assert mapper.itemMoveInfo({'itemMoveInfo': {
        'drop': False,
        'trade': True,
        'store': True,
        'cart': True,
        'sell': True,
        'mail': True,
        'auction': True,
        'guildStore': True
    }}) == {'Override': 100, 'NoDrop': True}
