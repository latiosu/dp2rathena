import bisect
import importlib
import json

import tortilla
import yaml

from dp2rathena import item_mapper

class Converter:
    def __init__(self, api_key, debug=False):
        self.api = tortilla.wrap('https://divine-pride.net/api/database', debug=debug)
        self.api.config.params.apiKey = api_key
        self.mapper = item_mapper.Mapper()

    def fetch_item(self, itemid):
        try:
            return self.api.item.get(itemid)
        except IOError as err:
            if str(err).startswith('404'):
                return {'Id': int(itemid), 'Error': 'Item not found'}
            raise err

    def wrap_result(self, items):
        return {
            'Header': {
                'Type': 'ITEM_DB',
                'Version': 1,
            },
            'Body': items,
        }

    def convert_item(self, itemids, sort=False, wrap=True):
        items = list()
        for itemid in itemids:
            items.append(self.mapper.map_item(self.fetch_item(itemid)))
        if sort:
            items.sort(key=lambda item: item['Id'])
        if wrap:
            items = self.wrap_result(items)
        return yaml.dump(items, sort_keys=False)

    def fetch_mob(self, mobid):
        try:
            return self.api.monster.get(mobid)
        except IOError as err:
            if str(err).startswith('404'):
                return f'Id: {int(mobid)}, Error: Mob not found'
            raise err

    def convert_mob_skill(self, mobids):
        mobs = list()
        for mobid in mobids:
            mobs.append(self.mapper.map_mob_skill(self.fetch_mob(mobid)))
        return '\n'.join(mobs)