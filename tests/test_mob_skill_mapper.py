import os

import json
import pytest

from dp2rathena import mob_skill_mapper


# Shared instance to reduce startup time
mapper = mob_skill_mapper.Mapper()


def test_dummy_value(fixture):
    mob1002 = json.loads(open(fixture('mob_1002.json')).read())
    generated = mapper._dummy_value(mob1002['skill'][1], mob1002)
    assert generated == 'Poring@NPC_EMOTION'
    generated = mapper._dummy_value(mob1002['skill'][2], mob1002)
    assert generated == 'Poring@NPC_WATERATTACK'
    mob1049 = json.loads(open(fixture('mob_1049.json')).read())
    generated = mapper._dummy_value(mob1049['skill'][0], mob1049)
    assert generated == 'Picky@NPC_EMOTION'
    generated = mapper._dummy_value(mob1049['skill'][1], mob1049)
    assert generated == 'Picky@NPC_FIREATTACK'


def test_status():
    return None


def test_id():
    return None


def test_level():
    return None


def test_chance():
    return None


def test_casttime():
    return None


def test_delay():
    return None


def test_interruptable():
    return None


def test_target():
    return None


def test_condition():
    return None


def test_condition_value():
    return None


def test_val_1():
    return None


def test_val_2():
    return None


def test_val_3():
    return None


def test_val_4():
    return None


def test_val_5():
    return None


def test_send_emote():
    return None


def test_send_chat():
    return None


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


def test_map_mob_skill():
    with pytest.raises(AssertionError):
        mapper.map_mob_skill({})
    assert mapper.map_mob_skill(None) is None
    assert mapper.map_mob_skill({'Error': 'message'}) == {'Error': 'message'}
