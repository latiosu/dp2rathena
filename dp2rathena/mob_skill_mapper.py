from enum import Enum

import copy
import os
import re
import yaml


class Mapper:
    def __init__(self):
        # Lazy load skill_db until required
        self.skill_db = None

        # Structure = {'AL_TELEPORT': 26}
        self.skill_name_db = dict()

        self.schema = {
            'MobId': self._id,
            'Dummy': self._dummy_value,        # Rathena info value
            'State': self._status,             # State that triggers skill cast
            'SkillId': self._skillid,
            'SkillLv': self._level,
            'Rate': self._chance,              # Chance of skill cast when condition is met (10000 = 100%)
            'CastTime': self._casttime,        # Fixed cast time of skill
            'Delay': self._delay,              # Time (in ms) before attempting to recast the same skill
            'Cancelable': self._interruptable,
            'Target': self._target,            # Target of the skill
            'ConditionType': self._condition,  # Trigger condition of the skill
            'ConditionValue': self._condition_value,
            'Val1': self._val_1,
            'Val2': self._val_2,
            'Val3': self._val_3,
            'Val4': self._val_4,
            'Val5': self._val_5,
            'Emotion': self._send_emote,       # Emote used on skill cast
            'Chat': self._send_chat,           # Text output on skill cast
        }

        self.state_map = {
            # 'null': 'any',        # except dead; note 'anytarget' is RA shorthand notation and not used in DP
            'IDLE_ST': 'idle',      # in standby
            'RMOVE_ST': 'walk',     # in movement
            'DEAD_ST': 'dead',      # on kill
            'MOVEITEM_ST': 'loot',
            'BERSERK_ST': 'attack',
            'ANGRY_ST': 'angry',    # like attack, except player has not attacked mob yet
            'RUSH_ST': 'chase',     # following target, after being attacked
            'FOLLOW_ST': 'follow',  # following target, without being attacked
        }

        self.condition_map = {
            # 'null': 'always',                      # Unconditional (no condition value)
            'IF_HP': 'myhpltmaxrate',                # When mob's HP drops to the specified %
            'IF_HIDING': 'mystatuson',               # Currently only used for hiding in RA, If mob has the specified abnormality in status
            'IF_COMRADEHP': 'friendhpltmaxrate',     # When mob's friend's HP drops to the specified %
            'IF_COMRADECONDITION': 'friendstatuson', # If friend has the specified abnormality in status
            'IF_ENEMYCOUNT': 'attackpcge',           # When attack PCs become greater than or equal to the specified number
            'IF_SLAVENUM': 'slavele',                # When number of slaves is less than or equal to the original specified number
            'IF_RANGEATTACKED': 'longrangeattacked', # When long range attacked, ex. bows, guns, ranged skills (no condition value)
            'IF_SKILLUSE': 'skillused',              # When the specified skill is used on the mob
            'IF_MAGICLOCKED': 'casttargeted',        # When a target is in cast range (no condition value)
            'IF_RUDEATTACK': 'rudeattacked',         # When mob is rude attacked (no condition value)
            # Below types are RA-exclusive and aren't clearly mapped to DP data
            # - onspawn
            # - myhpinrate
            # - mystatusoff
            # - friendhpinrate
            # - friendstatusoff
            # - attackpcgt
            # - slavelt
            # - closedattacked
            # - afterskill
        }

        # Aegis monster mode mappings used by DP
        self.monster_mode_map = {
            'MONSTER_TYPE_01': 0x0081, # (passive)
            'MONSTER_TYPE_02': 0x0083, # (passive, looter)
            'MONSTER_TYPE_03': 0x1089, # (passive, assist and change-target melee)
            'MONSTER_TYPE_04': 0x3885, # (angry, change-target melee/chase)
            'MONSTER_TYPE_05': 0x2085, # (aggressive, change-target chase)
            'MONSTER_TYPE_06': 0x0000, # (passive, immobile, can't attack) [plants]
            'MONSTER_TYPE_07': 0x108B, # (passive, looter, assist, change-target melee)
            'MONSTER_TYPE_08': 0x7085, # (aggressive, change-target melee/chase, target weak enemies)
            'MONSTER_TYPE_09': 0x3095, # (aggressive, change-target melee/chase, cast sensor idle) [Guardian]
            'MONSTER_TYPE_10': 0x0084, # (aggressive, immobile)
            'MONSTER_TYPE_11': 0x0084, # (aggressive, immobile) [Guardian]
            'MONSTER_TYPE_12': 0x2085, # (aggressive, change-target chase) [Guardian]
            'MONSTER_TYPE_13': 0x308D, # (aggressive, change-target melee/chase, assist)
            'MONSTER_TYPE_17': 0x0091, # (passive, cast sensor idle)
            'MONSTER_TYPE_19': 0x3095, # (aggressive, change-target melee/chase, cast sensor idle)
            'MONSTER_TYPE_20': 0x3295, # (aggressive, change-target melee/chase, cast sensor idle/chase)
            'MONSTER_TYPE_21': 0x3695, # (aggressive, change-target melee/chase, cast sensor idle/chase, chase-change target)
            'MONSTER_TYPE_24': 0x00A1, # (passive, does not walk randomly) [Slave]
            'MONSTER_TYPE_25': 0x0001, # (passive, can't attack) [Pet]
            'MONSTER_TYPE_26': 0xB695, # (aggressive, change-target melee/chase, cast sensor idle/chase, chase-change target, random target)
            'MONSTER_TYPE_27': 0x8084, # (aggressive, immobile, random target)
        }

        self.summon_skills = [
            'NPC_SUMMONSLAVE',
            'NPC_SUMMONMONSTER',
            'NPC_DEATHSUMMON',
            'NPC_TRANSFORMATION',
            'NPC_METAMORPHOSIS',
        ]

        self.emote_skills = ['NPC_EMOTION', 'NPC_EMOTION_ON']

    # Used for lazy loading skill_db.yml as loading is slow
    def _require_skill_db(self):
        if self.skill_db is None:
            current_path = os.path.join(os.getcwd(), os.path.dirname(__file__))
            skill_db_path = os.path.join(os.path.realpath(current_path), 'db', 'skill_db.yml')
            self.skill_db = yaml.load(open(skill_db_path, encoding='utf-8'), Loader=yaml.FullLoader)

            for k, v in self.skill_db.items():
                self.skill_name_db[v['Name']] = k


    # Helper for checking skill db values
    def _skill_db_value(self, skillId, value):
        self._require_skill_db()
        if skillId in self.skill_db and value in self.skill_db[skillId]:
            return self.skill_db[skillId][value]
        return None

    def _id(self, data, parent_data = {}):
        return parent_data['id']

    def _dummy_value(self, data, parent_data):
        skill_name = self._skill_db_value(data['skillId'], 'Name')
        if skill_name is not None:
            return parent_data['name'] + '@' + skill_name
        return parent_data['name'] + '@Unknown Skill'

    def _status(self, data, parent_data = {}):
        if data['status'] is None:
            return 'any'
        elif data['status'] not in self.state_map:
            return None
        return self.state_map[data['status']]

    def _skillid(self, data, parent_data = {}):
        return data['skillId']

    def _level(self, data, parent_data):
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills:
            return len(parent_data['slaves'])
        return data['level']

    def _chance(self, data, parent_data = {}):
        return data['chance'] * 10

    def _casttime(self, data, parent_data = {}):
        return data['casttime']

    def _delay(self, data, parent_data = {}):
        return data['delay']

    def _interruptable(self, data, parent_data = {}):
        return 'yes' if data['interruptable'] else 'no'

    def _target(self, data, parent_data = {}):
        if data['condition'] == 'IF_COMRADEHP' \
            or data['condition'] == 'IF_COMRADECONDITION':
            return 'friend'
        elif self._skill_db_value(data['skillId'], 'TargetType') == 'Self':
            return 'self'
        return 'target' # Default value, other types unclear from DP data

    def _condition(self, data, parent_data = {}):
        if data['condition'] is None \
            or data['condition'] not in self.condition_map:
            return 'always'
        return self.condition_map[data['condition']]

    def _condition_value(self, data, parent_data = {}):
        if data['condition'] == 'IF_HIDING':
            return 'hiding'
        elif data['conditionValue'] == 'BODY_ALL':
            return 'anybad'
        elif data['condition'] == 'IF_SKILLUSE' and data['conditionValue'] != None:
            return self.skill_name_db[data['conditionValue']]
        elif data['condition'] not in self.condition_map:
            return 0
        # Other statuses have no current use-cases in rathena or DP
        return data['conditionValue']

    def _val_1(self, data, parent_data):
        # Summoned monster no. 1
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills \
            and len(parent_data['slaves']) >= 1:
            return parent_data['slaves'][0]['id']
        # NPC_EMOTION is mapped by val1 in RA, otherwise send_emote is used
        if self._skill_db_value(data['skillId'], 'Name') in self.emote_skills:
            return data['sendValue']
        return None

    def _val_2(self, data, parent_data):
        # Summoned monster no. 2
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills \
            and len(parent_data['slaves']) >= 2:
            return parent_data['slaves'][1]['id']
        return None

    def _val_3(self, data, parent_data):
        # Summoned monster no. 3
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills \
            and len(parent_data['slaves']) >= 3:
            return parent_data['slaves'][2]['id']
        return None

    def _val_4(self, data, parent_data):
        # Summoned monster no. 4
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills \
            and len(parent_data['slaves']) >= 4:
            return parent_data['slaves'][3]['id']
        return None

    def _val_5(self, data, parent_data):
        # Summoned monster no. 5
        if self._skill_db_value(data['skillId'], 'Name') in self.summon_skills \
            and len(parent_data['slaves']) >= 5:
            return parent_data['slaves'][4]['id']
        return None

    # Used whenever val1 is required for another purpose
    def _send_emote(self, data, parent_data):
        if self._skill_db_value(data['skillId'], 'Name') not in self.emote_skills \
            and data['sendType'] == 'SEND_EMOTICON':
            return data['sendValue']
        return None

    def _send_chat(self, data, parent_data = {}):
        if data['sendType'] == 'SEND_CHAT':
            return data['sendValue']
        return None

    def _map_schema(self, schema, data, parent_data):
        if schema is None:
            return None
        elif data is None:
            return schema
        result = copy.deepcopy(schema)
        for k, v in schema.items():
            if callable(v):
                result[k] = v(data, parent_data)
            elif type(v) is dict:
                result[k] = self._map_schema(v, data, parent_data)
            elif (type(v) is str or type(v) is int) and v in data:
                result[k] = data[v]
            else:
                result[k] = v
        return result

    def map_mob_skill(self, data):
        if data is None or 'Error' in data:
            return data
        skills = list()
        for skill in data['skill']:
            skills.append(self._map_schema(self.schema, skill, data))
        return skills
