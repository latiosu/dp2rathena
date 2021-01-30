import os

import pytest

from dp2rathena import mob_skill_mapper


def test_dummy_value():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_status():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_id():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_level():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_chance():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_casttime():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_delay():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_interruptable():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_target():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_condition():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_condition_value():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_val_1():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_val_2():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_val_3():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_val_4():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_val_5():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_send_emote():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_send_chat():
    mapper = mob_skill_mapper.Mapper()
    return None


def test_map_schema():
    mapper = mob_skill_mapper.Mapper()
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


def test_map_mob_skill():
    mapper = mob_skill_mapper.Mapper()
    with pytest.raises(AssertionError):
        mapper.map_mob_skill({})
    assert mapper.map_mob_skill(None) is None
    assert mapper.map_mob_skill({'Error': 'message'}) == {'Error': 'message'}
