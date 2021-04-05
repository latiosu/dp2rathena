import os

import pytest

from dp2rathena import mob_mapper


# Shared instance to reduce load times
mapper = mob_mapper.Mapper()


def test_mapping_sp():
    with pytest.raises(AssertionError):
        mapper._sp({'stats':{}})
        mapper._sp({'stats':{'sp': -1}})
    assert mapper._sp({'stats':{'sp': 1}}) is None
    assert mapper._sp({'stats':{'sp': 0}}) == 0
    assert mapper._sp({'stats':{'sp': 2}}) == 2


# Scale
# 0 - Small (default)
# 1 - Medium
# 2 - Large
def test_mapping_scale():
    with pytest.raises(AssertionError):
        mapper._scale({'stats':{}})
        mapper._scale({'stats':{'scale': -1}})
        mapper._scale({'stats':{'scale': 3}})
    assert mapper._scale({'stats':{'scale': 0}}) == 'Small'
    assert mapper._scale({'stats':{'scale': 1}}) == 'Medium'
    assert mapper._scale({'stats':{'scale': 2}}) == 'Large'


# Race
# 0 - Formless (Default)
# 1 - Undead
# 2 - Brute
# 3 - Plant
# 4 - Insect
# 5 - Fish
# 6 - Demon
# 7 - Demihuman
# 8 - Angel
# 9 - Dragon
def test_mapping_race():
    with pytest.raises(AssertionError):
        mapper._race({'stats':{}})
        mapper._race({'stats':{'race': -1}})
        mapper._race({'stats':{'race': 10}})
    assert mapper._race({'stats':{'race': 0}}) == 'Formless'
    assert mapper._race({'stats':{'race': 1}}) == 'Undead'
    assert mapper._race({'stats':{'race': 2}}) == 'Brute'
    assert mapper._race({'stats':{'race': 3}}) == 'Plant'
    assert mapper._race({'stats':{'race': 4}}) == 'Insect'
    assert mapper._race({'stats':{'race': 5}}) == 'Fish'
    assert mapper._race({'stats':{'race': 6}}) == 'Demon'
    assert mapper._race({'stats':{'race': 7}}) == 'Demihuman'
    assert mapper._race({'stats':{'race': 8}}) == 'Angel'
    assert mapper._race({'stats':{'race': 9}}) == 'Dragon'


# Element is x % 10
# 0 - Neutral (Default)
# 1 - Water
# 2 - Earth
# 3 - Fire
# 4 - Wind
# 5 - Poison
# 6 - Holy
# 7 - Shadow
# 8 - Ghost
# 9 - Undead
def test_mapping_element():
    with pytest.raises(AssertionError):
        mapper._element({'stats':{}})
        mapper._element({'stats':{'element': -1}})
        mapper._element({'stats':{'element': 19}})
        mapper._element({'stats':{'element': 90}})
    assert mapper._element({'stats':{'element': 20}}) == 'Neutral'
    assert mapper._element({'stats':{'element': 21}}) == 'Water'
    assert mapper._element({'stats':{'element': 22}}) == 'Earth'
    assert mapper._element({'stats':{'element': 23}}) == 'Fire'
    assert mapper._element({'stats':{'element': 24}}) == 'Wind'
    assert mapper._element({'stats':{'element': 25}}) == 'Poison'
    assert mapper._element({'stats':{'element': 26}}) == 'Holy'
    assert mapper._element({'stats':{'element': 27}}) == 'Dark'
    assert mapper._element({'stats':{'element': 28}}) == 'Ghost'
    assert mapper._element({'stats':{'element': 29}}) == 'Undead'
    assert mapper._element({'stats':{'element': 80}}) == 'Neutral'
    assert mapper._element({'stats':{'element': 81}}) == 'Water'
    assert mapper._element({'stats':{'element': 82}}) == 'Earth'
    assert mapper._element({'stats':{'element': 83}}) == 'Fire'
    assert mapper._element({'stats':{'element': 84}}) == 'Wind'
    assert mapper._element({'stats':{'element': 85}}) == 'Poison'
    assert mapper._element({'stats':{'element': 86}}) == 'Holy'
    assert mapper._element({'stats':{'element': 87}}) == 'Dark'
    assert mapper._element({'stats':{'element': 88}}) == 'Ghost'
    assert mapper._element({'stats':{'element': 89}}) == 'Undead'


# Element Level is int(x / 20) and value between 1-4
def test_mapping_elementLevel():
    with pytest.raises(AssertionError):
        mapper._elementLevel({'stats':{}})
        mapper._elementLevel({'stats':{'element': -1}})
        mapper._element({'stats':{'element': 19}})
        mapper._element({'stats':{'element': 90}})
    assert mapper._elementLevel({'stats':{'element': 20}}) == 1
    assert mapper._elementLevel({'stats':{'element': 21}}) == 1
    assert mapper._elementLevel({'stats':{'element': 22}}) == 1
    assert mapper._elementLevel({'stats':{'element': 23}}) == 1
    assert mapper._elementLevel({'stats':{'element': 24}}) == 1
    assert mapper._elementLevel({'stats':{'element': 25}}) == 1
    assert mapper._elementLevel({'stats':{'element': 26}}) == 1
    assert mapper._elementLevel({'stats':{'element': 27}}) == 1
    assert mapper._elementLevel({'stats':{'element': 28}}) == 1
    assert mapper._elementLevel({'stats':{'element': 29}}) == 1
    assert mapper._elementLevel({'stats':{'element': 80}}) == 4
    assert mapper._elementLevel({'stats':{'element': 81}}) == 4
    assert mapper._elementLevel({'stats':{'element': 82}}) == 4
    assert mapper._elementLevel({'stats':{'element': 83}}) == 4
    assert mapper._elementLevel({'stats':{'element': 84}}) == 4
    assert mapper._elementLevel({'stats':{'element': 85}}) == 4
    assert mapper._elementLevel({'stats':{'element': 86}}) == 4
    assert mapper._elementLevel({'stats':{'element': 87}}) == 4
    assert mapper._elementLevel({'stats':{'element': 88}}) == 4
    assert mapper._elementLevel({'stats':{'element': 89}}) == 4


def test_mapping_damageTaken():
    with pytest.raises(AssertionError):
        mapper._damageTaken({'stats':{}})
        mapper._damageTaken({'stats':{'mvp': ''}})
        mapper._damageTaken({'stats':{'mvp': -1}})
    assert mapper._damageTaken({'stats':{'mvp': 0}}) is None
    assert mapper._damageTaken({'stats':{'mvp': 1}}) == 10


def test_mapping_ai():
    with pytest.raises(AssertionError):
        mapper._ai({'stats':{}})
        mapper._ai({'stats':{'ai': 'Unknown'}})
    assert mapper._ai({'stats':{'ai': ''}}) == 'Unknown'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_01'}}) == '01'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_02'}}) == '02'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_03'}}) == '03'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_04'}}) == '04'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_05'}}) == '05'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_06'}}) == '06'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_07'}}) == '07'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_08'}}) == '08'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_09'}}) == '09'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_10'}}) == '10'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_11'}}) == '11'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_12'}}) == '12'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_13'}}) == '13'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_17'}}) == '17'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_19'}}) == '19'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_20'}}) == '20'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_21'}}) == '21'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_24'}}) == '24'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_25'}}) == '25'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_26'}}) == '26'
    assert mapper._ai({'stats':{'ai': 'MONSTER_TYPE_27'}}) == '27'


# Class
# 0 - Normal (default)
# 1 - Boss
# 2 - Guardian
# 4 - Battlefield
# 5 - Event
def test_mapping_class():
    with pytest.raises(AssertionError):
        mapper._class({'stats':{}})
        mapper._class({'stats':{'class': -1}})
        mapper._class({'stats':{'class': 3}})
        mapper._class({'stats':{'class': 6}})
    assert mapper._class({'stats':{'class': 0}}) is None
    assert mapper._class({'stats':{'class': 1}}) == 'Boss'
    assert mapper._class({'stats':{'class': 2}}) == 'Guardian'
    assert mapper._class({'stats':{'class': 4}}) == 'Battlefield'
    assert mapper._class({'stats':{'class': 5}}) == 'Event'


def test_mapping_mvpdrops():
    with pytest.raises(AssertionError):
        mapper._drops({}, 'mvpdrops')
        mapper._drops({'mvpdrops': -1}, 'mvpdrops')
    assert mapper._drops({'mvpdrops': []}, 'mvpdrops') == None
    assert mapper._drops({'mvpdrops': [{'itemId': 25159, 'chance': 1250, 'stealProtected': False}]}, 'mvpdrops') \
        == [{'Item': 'Heart_Hunter_Seal', 'Rate': 1250}]


def test_mapping_drops():
    with pytest.raises(AssertionError):
        mapper._drops({})
        mapper._drops({'drops': -1})
    assert mapper._drops({'drops': []}) == None
    assert mapper._drops({'drops': [{'itemId': 501, 'chance': 0, 'stealProtected': False}]}) == None
    assert mapper._drops({'drops': [{'itemId': -1, 'chance': 1, 'stealProtected': False}]}) \
        == [{'Item': -1, 'Rate': 1}]
    assert mapper._drops({'drops': [{'itemId': 25159, 'chance': 1250, 'stealProtected': False}]}) \
        == [{'Item': 'Heart_Hunter_Seal', 'Rate': 1250}]
    assert mapper._drops({'drops': [{'itemId': 6213, 'chance': 30, 'stealProtected': False}, \
                                    {'itemId': 27306, 'chance': 1, 'stealProtected': True}]}) \
        == [{'Item': 'Explosive_Powder', 'Rate': 30}, \
            {'Item': 'Bellare_Card', 'Rate': 1, 'StealProtected': True}]


def test_map_schema():
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


def test_map_mob(fixture):
    assert mapper.map_mob(None) is None
    assert mapper.map_mob({'id': 1, 'dbname': 'x'}) == {'Id': 1, 'AegisName': 'x', 'Error': 'Mob stat data missing'}
    assert mapper.map_mob({'id': 1, 'dbname': 'x', 'stats': {}}) \
        == {'Id': 1, 'AegisName': 'x', 'Error': 'Mob stat data missing'}
    assert mapper.map_mob({'id': 1, 'dbname': 'x', 'stats': {'level': 9}}) \
        == {'Id': 1, 'AegisName': 'x', 'Error': 'General mob data missing'}
    assert mapper.map_mob({'Error': 'message'}) == {'Error': 'message'}
