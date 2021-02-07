import os

import json
import pytest

from dp2rathena import mob_skill_mapper


# Shared instances to reduce startup time
mapper = mob_skill_mapper.Mapper()
current_path = os.path.join(os.getcwd(), os.path.dirname(__file__))
fixtures_path = os.path.join(os.path.realpath(current_path), 'fixtures')
poring = json.loads(open(os.path.join(fixtures_path, 'mob_1002.json')).read())
poring_emote = poring['skill'][1]
poring_water = poring['skill'][2]
picky = json.loads(open(os.path.join(fixtures_path, 'mob_1049.json')).read())
picky_emote = picky['skill'][0]
picky_fire = picky['skill'][1]


def test_dummy_value(fixture):
    assert mapper._dummy_value(poring_emote, poring) == 'Poring@NPC_EMOTION'
    assert mapper._dummy_value(poring_water, poring) == 'Poring@NPC_WATERATTACK'
    assert mapper._dummy_value(picky_emote, picky) == 'Picky@NPC_EMOTION'
    assert mapper._dummy_value(picky_fire, picky) == 'Picky@NPC_FIREATTACK'


def test_status():
    assert mapper._status(poring_emote) == 'loot'
    assert mapper._status(poring_water) == 'attack'
    assert mapper._status(picky_emote) == 'walk'
    assert mapper._status(picky_fire) == 'attack'
    assert mapper._status({'status': None}) == 'any'
    assert mapper._status({'status': 'IDLE_ST'}) == 'idle'


def test_id():
    assert mapper._id(poring_emote) == 197
    assert mapper._id(poring_water) == 184
    assert mapper._id(picky_emote) == 197
    assert mapper._id(picky_fire) == 186
    assert mapper._id({'skillId': 0}) == 0


def test_level():
    assert mapper._level(poring_emote) == 1
    assert mapper._level(poring_water) == 1
    assert mapper._level(picky_emote) == 1
    assert mapper._level(picky_fire) == 1
    assert mapper._level({'level': 0}) == 0


def test_chance():
    assert mapper._chance(poring_emote) == 2000
    assert mapper._chance(poring_water) == 2000
    assert mapper._chance(picky_emote) == 2000
    assert mapper._chance(picky_fire) == 2000
    assert mapper._chance({'chance': 0}) == 0
    assert mapper._chance({'chance': 10}) == 100


def test_casttime():
    assert mapper._casttime(poring_emote) == 0
    assert mapper._casttime(poring_water) == 0
    assert mapper._casttime(picky_emote) == 0
    assert mapper._casttime(picky_fire) == 0
    assert mapper._casttime({'casttime': 1000}) == 1000


def test_delay():
    assert mapper._delay(poring_emote) == 5000
    assert mapper._delay(poring_water) == 5000
    assert mapper._delay(picky_emote) == 5000
    assert mapper._delay(picky_fire) == 5000
    assert mapper._delay({'delay': 0}) == 0


def test_interruptable():
    assert mapper._interruptable(poring_emote) == 'yes'
    assert mapper._interruptable(poring_water) == 'yes'
    assert mapper._interruptable(picky_emote) == 'yes'
    assert mapper._interruptable(picky_fire) == 'yes'
    assert mapper._interruptable({'interruptable': False}) == 'no'


def test_target():
    assert mapper._target(poring_emote) == 'self'
    assert mapper._target(poring_water) == 'target'
    assert mapper._target(picky_emote) == 'self'
    assert mapper._target(picky_fire) == 'target'
    assert mapper._target({'condition': None, 'skillId': 1}) == 'target'
    assert mapper._target({'condition': 'IF_HP', 'skillId': 1}) == 'target'
    assert mapper._target({'condition': None, 'skillId': 7}) == 'self'
    assert mapper._target({'condition': 'IF_COMRADEHP'}) == 'friend'
    assert mapper._target({'condition': 'IF_COMRADECONDITION'}) == 'friend'


def test_condition():
    assert mapper._condition(poring_emote) == 'always'
    assert mapper._condition(poring_water) == 'always'
    assert mapper._condition(picky_emote) == 'always'
    assert mapper._condition(picky_fire) == 'always'
    assert mapper._condition({'condition': None}) == 'always'
    assert mapper._condition({'condition': 'IF_HP'}) == 'myhpltmaxrate'
    assert mapper._condition({'condition': 'IF_COMRADEHP'}) == 'friendhpltmaxrate'
    assert mapper._condition({'condition': 'IF_COMRADECONDITION'}) == 'friendstatuson'


def test_condition_value():
    assert mapper._condition_value(poring_emote) == 0
    assert mapper._condition_value(poring_water) == 0
    assert mapper._condition_value(picky_emote) == 0
    assert mapper._condition_value(picky_fire) == 0
    assert mapper._condition_value({'condition': None, 'conditionValue': None}) == 0
    assert mapper._condition_value({'condition': None, 'conditionValue': 0}) == 0
    assert mapper._condition_value({'condition': None, 'conditionValue': 5}) == 5
    assert mapper._condition_value({'condition': 'IF_HIDING'}) == 'hiding'
    assert mapper._condition_value({'condition': None, 'conditionValue': 'BODY_ALL'}) == 'anybad'


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
    assert mapper._send_emote(poring_emote) == '2'
    assert mapper._send_emote(poring_water) == None
    assert mapper._send_emote(picky_emote) == '2'
    assert mapper._send_emote(picky_fire) == None
    assert mapper._send_emote({'sendType': 'SEND_EMOTICON', 'sendValue': 2}) == 2


def test_send_chat():
    assert mapper._send_chat(poring_emote) == None
    assert mapper._send_chat(poring_water) == None
    assert mapper._send_chat(picky_emote) == None
    assert mapper._send_chat(picky_fire) == None
    assert mapper._send_chat({'sendType': 'SEND_CHAT', 'sendValue': 5}) == 5


def test_map_schema():
    assert mapper._map_schema(None, None, None) is None
    assert mapper._map_schema({}, None, None) == {}
    assert mapper._map_schema(None, {}, None) is None
    assert mapper._map_schema(None, None, {}) is None
    assert mapper._map_schema({}, {}, None) == {}
    assert mapper._map_schema(None, {}, {}) is None
    assert mapper._map_schema({}, None, {}) == {}
    assert mapper._map_schema({}, {}, {}) == {}
    assert mapper._map_schema({'x': None}, {}, {}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': 0}, {}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': None}, {}) == {}
    assert mapper._map_schema({'x': 'to_map'}, {'to_map': 'y'}, {}) == {'x': 'y'}
    assert mapper._map_schema({'x': lambda x: None}, {'y': 'z'}, {}) == {}
    assert mapper._map_schema({'x': {'y': 'to_map'}}, {'to_map': 'z'}, {}) == {'x': {'y': 'z'}}
    assert mapper._map_schema({'x': 1}, {'not_mapped': 'value'}, {}) == {}
    assert mapper._map_schema({'x': 1}, {1: 'y'}, {}) == {'x': 'y'}
    assert mapper._map_schema({1.0: 1}, {1: 'y'}, {}) == {1.0: 'y'}
    assert mapper._map_schema({'x': 1.0}, {'not_mapped': 'value'}, {}) == {'x': 1.0}


def test_map_mob_skill():
    with pytest.raises(KeyError):
        mapper.map_mob_skill({})
    assert mapper.map_mob_skill(None) is None
    assert mapper.map_mob_skill({'Error': 'message'}) == {'Error': 'message'}
