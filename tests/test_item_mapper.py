import os

import pytest

from dp2rathena import item_mapper


def test_mapping_name():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        assert mapper._name({}) == ''
    assert mapper._name({'name': None}) == ''
    assert mapper._name({'name': ''}) == ''
    assert mapper._name({'name': '100T Zeny Check'}) == '100T Zeny Check'
    assert mapper._name({'name': 'Knife [4]'}) == 'Knife'
    assert mapper._name({'name': 'Hunting Bow [2]'}) == 'Hunting Bow'
    assert mapper._name({'name': '[Katsua]Adventurer\'s Backpack [1]'}) == '[Katsua]Adventurer\'s Backpack'
    assert mapper._name({'name': 'Travel Brochure [Amatsu]'}) == 'Travel Brochure [Amatsu]'
    assert mapper._name({'name': 'MATK+1%(Lower)'}) == 'MATK+1%(Lower)'


def test_mapping_itemTypeId():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._itemTypeId({})
        mapper._itemTypeId({'itemTypeId': 0})
        mapper._itemTypeId({'itemSubTypeId': 0})
        mapper._itemTypeId({'itemTypeId': -1, 'itemSubTypeId': -1})
        mapper._itemTypeId({'itemTypeId': 1, 'itemSubTypeId': -1})
    assert mapper._itemTypeId({'itemTypeId': 0, 'itemSubTypeId': 0}) is None
    assert mapper._itemTypeId({'itemTypeId': 1, 'itemSubTypeId': 0}) == 'Weapon'
    assert mapper._itemTypeId({'itemTypeId': 2, 'itemSubTypeId': 518, 'name': 'Isis Egg'}) == 'PetEgg'
    assert mapper._itemTypeId({'itemTypeId': 2, 'itemSubTypeId': 518, 'name': 'Broken Shell'}) == 'PetArmor'
    assert mapper._itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 0}) == 'Consumable'
    assert mapper._itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 768}) == 'Healing/Usable/DelayConsume/Cash'
    assert mapper._itemTypeId({'itemTypeId': 3, 'itemSubTypeId': 769}) == 'Healing'
    assert mapper._itemTypeId({'itemTypeId': 9, 'itemSubTypeId': 0}) == 'Armor'
    assert mapper._itemTypeId({'itemTypeId': 10, 'itemSubTypeId': 0}) == 'ShadowGear'


def test_mapping_itemSubTypeId():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._itemTypeId({})
        mapper._itemTypeId({'itemTypeId': 0})
        mapper._itemTypeId({'itemSubTypeId': 0})
        mapper._itemSubTypeId({'itemTypeId': -1, 'itemSubTypeId': -1})
        mapper._itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': -1})
    assert mapper._itemSubTypeId({'itemTypeId': 0, 'itemSubTypeId': 0}) is None
    assert mapper._itemSubTypeId({'itemTypeId': 4, 'itemSubTypeId': 1025}) \
        == 'Arrow/Dagger/Bullet/Shell/Grenade/Shuriken/Kunai/CannonBall/ThrowWeapon'
    assert mapper._itemSubTypeId({'itemTypeId': 4, 'itemSubTypeId': 0}) \
        == 'Arrow/Dagger/Bullet/Shell/Grenade/Shuriken/Kunai/CannonBall/ThrowWeapon'
    assert mapper._itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': 258}) == '2hSword'
    assert mapper._itemSubTypeId({'itemTypeId': 1, 'itemSubTypeId': 0}) is None
    assert mapper._itemSubTypeId({'itemTypeId': 2, 'itemSubTypeId': 512}) is None
    assert mapper._itemSubTypeId({'itemTypeId': 10, 'itemSubTypeId': 526}) is None


def test_mapping_sell():
    mapper = item_mapper.Mapper()
    assert mapper._sell({}) is None


def test_mapping_weight():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._weight({})
    assert mapper._weight({'weight': 0}) == 0
    assert mapper._weight({'weight': 50.0}) == 500
    assert mapper._weight({'weight': 0.1}) == 1
    assert mapper._weight({'weight': -1}) == 0


def test_mapping_job():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._job({})
        mapper._job({'job': -1})
        mapper._job({'job': 0x100000})
    assert mapper._job({'job': None}) is None
    assert mapper._job({'job': 0xFFFFF}) is None
    assert mapper._job({'job': 0}) is None
    assert mapper._job({'job': 0x20410}) == {'Acolyte': True, 'Monk': True, 'Priest': True}
    assert mapper._job({'job': 1}) == {'Novice': True, 'SuperNovice': True}
    assert mapper._job({'job': 142}) == {'Summoner': True}
    assert mapper._job({'job': 144}) == {'KagerouOboro': True, 'Rebellion': True}


def test_mapping_classNum():
    mapper = item_mapper.Mapper()
    assert mapper._classNum({}) is None
    assert mapper._classNum({'classNum': 0}) is None
    assert mapper._classNum({'classNum': -1}) is None


def test_mapping_gender():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._gender({})
        mapper._gender({'job': -1})
        mapper._gender({'job': 0x100000})
    assert mapper._gender({'job': None}) is None
    assert mapper._gender({'job': 1}) is None
    assert mapper._gender({'job': 0xFFFFF}) is None
    assert mapper._gender({'job': 0x08000}) == 'Male'
    assert mapper._gender({'job': 0x10000}) == 'Female'
    assert mapper._gender({'job': 0x18000}) == 'Both'


def test_mapping_locationId():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._locationId({})
        mapper._locationId({'locationId': 0})
        mapper._locationId({'itemTypeId': 0})
        mapper._locationId({'locationId': -1, 'itemTypeId': 0})
        mapper._locationId({'locationId': 0x400000, 'itemTypeId': 0})
    assert mapper._locationId({'locationId': None, 'itemTypeId': 0}) is None
    assert mapper._locationId({'locationId': 0, 'itemTypeId': 0}) is None
    assert mapper._locationId({'locationId': 0x10, 'itemTypeId': 0}) == {'Armor': True}
    assert mapper._locationId({'locationId': 0, 'itemTypeId': 4}) == {'Ammo': True}
    assert mapper._locationId({'locationId': 0x22, 'itemTypeId': 0}) == {'Both_Hand': True}
    assert mapper._locationId({'locationId': 0x88, 'itemTypeId': 0}) == {'Both_Accessory': True}
    assert mapper._locationId({'locationId': 0x10000, 'itemTypeId': 0}) == {'Shadow_Armor': True}
    assert mapper._locationId({'locationId': 0x400, 'itemTypeId': 0}) == {'Costume_Head_Top': True}
    assert mapper._locationId({'locationId': 0x300, 'itemTypeId': 0}) \
        == {'Head_Top': True, 'Head_Mid': True}
    assert mapper._locationId({'locationId': 0x301, 'itemTypeId': 0}) \
        == {'Head_Top': True, 'Head_Mid': True, 'Head_Low': True}


def test_mapping_itemLevel():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._itemLevel({})
        mapper._itemLevel({'itemLevel': -1})
        mapper._itemLevel({'itemLevel': 5})
    assert mapper._itemLevel({'itemLevel': 0}) is None
    assert mapper._itemLevel({'itemLevel': 1}) == 1
    assert mapper._itemLevel({'itemLevel': 4}) == 4


def test_mapping_itemMoveInfo():
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper._itemMoveInfo({})
    assert mapper._itemMoveInfo({'itemMoveInfo': {
        'drop': True,
        'trade': True,
        'store': True,
        'cart': True,
        'sell': True,
        'mail': True,
        'auction': True,
        'guildStore': True
    }}) is None
    assert mapper._itemMoveInfo({'itemMoveInfo': {
        'drop': False,
        'trade': True,
        'store': True,
        'cart': True,
        'sell': True,
        'mail': True,
        'auction': True,
        'guildStore': True
    }}) == {'Override': 100, 'NoDrop': True}


def test_map_schema():
    mapper = item_mapper.Mapper()
    assert mapper._map_schema(None, None) is None
    assert mapper._map_schema(None, {}) is None
    assert mapper._map_schema({}, None) == {}
    assert mapper._map_schema({}, {}) == {}
    assert mapper._map_schema({'x': None}, {}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': 0}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': None}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': 'y'}) == {'x': 'y'}
    assert mapper._map_schema({'x': lambda x: None}, {'y': 'z'}) == {}
    assert mapper._map_schema({'x': len}, {'y': 'z'}) == {'x': 1}
    assert mapper._map_schema({'x': {'y': 'to_map'}}, {'to_map': 'z'}) == {'x': {'y': 'z'}}
    assert mapper._map_schema({'x': 1}, {'not_mapped': 'value'}) == {}
    assert mapper._map_schema({'x': 1}, {1: 'y'}) == {'x': 'y'}
    assert mapper._map_schema({1.0: 1}, {1: 'y'}) == {1.0: 'y'}
    assert mapper._map_schema({'x': 1.0}, {'not_mapped': 'value'}) == {'x': 1.0}


def test_map_item(fixture):
    mapper = item_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper.map_item({})
    assert mapper.map_item(None) is None
    assert mapper.map_item({'Error': 'message'}) == {'Error': 'message'}
