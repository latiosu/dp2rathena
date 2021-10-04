import bisect
import importlib
import json
import re

import tortilla
import yaml

from dp2rathena import item_mapper
from dp2rathena import mob_skill_mapper
from dp2rathena import mob_mapper

class Converter:
    def __init__(self, api_key, debug=False):
        self.api = tortilla.wrap('https://divine-pride.net/api/database', debug=debug)
        self.api.config.params.apiKey = api_key

    def fetch_item(self, itemid):
        try:
            return self.api.item.get(itemid)
        except IOError as err:
            if str(err).startswith('404'):
                return {'Id': int(itemid), 'Error': 'Item not found'}
            raise err

    def convert_item(self, itemids, sort=False, wrap=True):
        mapper = item_mapper.Mapper()
        items = list()
        for itemid in itemids:
            if type(itemid) is int or itemid.isnumeric():
                items.append(mapper.map_item(self.fetch_item(itemid)))
        if sort:
            items.sort(key=lambda item: item['Id'])
        if wrap:
            items = {
                'Header': {
                    'Type': 'ITEM_DB',
                    'Version': 1,
                },
                'Body': items,
            }
        return yaml.dump(items, sort_keys=False)

    def fetch_mob(self, mobid):
        try:
            return self.api.monster.get(mobid)
        except IOError as err:
            if str(err).startswith('404'):
                return f'Id: {int(mobid)}, Error: Mob not found'
            raise err

    def convert_mob_skill(self, mobids, comment=True):
        mapper = mob_skill_mapper.Mapper()
        all_mob_skills = list()
        for mobid in mobids:
            if type(mobid) is int or mobid.isnumeric():
                all_mob_skills.append(mapper.map_mob_skill(self.fetch_mob(mobid)))

        result = ''
        for mob_skills in all_mob_skills:
            for skill in mob_skills:
                if skill['SkillLv'] < 0:
                    continue
                elif comment and 'Unknown Skill' in skill['Dummy']:
                    result += '//'
                for value in skill.values():
                    result += ('' if value is None else str(value)) + ','
                result = result[:-1] + '\n'
        return result

    def convert_mob(self, mobids, sort=False, wrap=True):
        mapper = mob_mapper.Mapper()
        mobs = list()
        for mobid in mobids:
            if type(mobid) is int or mobid.isnumeric():
                mobs.append(mapper.map_mob(self.fetch_mob(mobid)))
        if sort:
            mobs.sort(key=lambda mob: mob['Id'])
        if wrap:
            mobs = {
                'Header': {
                    'Type': 'MOB_DB',
                    'Version': 2,
                },
                'Body': mobs,
            }
        return self.remove_numerical_quotes(yaml.dump(mobs, sort_keys=False))

    def remove_numerical_quotes(self, payload):
        return re.sub(r'(.*)\'(\d+)\'(.*)', r'\1\2\3', payload)
