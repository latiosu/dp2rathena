import bisect
import importlib
import json
import os

import tortilla
import yaml

from dp2rathena import item_mapper

class Converter:
    def __init__(self, debug=False):
        self.api = tortilla.wrap('https://divine-pride.net/api/database', debug=debug)
        if 'DIVINEPRIDE_API_KEY' not in os.environ:
            exit('API key missing from .env')
        self.api.config.params.apiKey = os.getenv('DIVINEPRIDE_API_KEY')
        self.mapper = item_mapper.Mapper()

    def fetch_item(self, itemid):
        try:
            return self.api.item.get(itemid)
        except IOError as err:
            if str(err).startswith('404'):
                return {'Id': itemid, 'Error': 'Item not found'}
            raise err

    def wrap_result(self, items):
        return {
            'Header': {
                'Type': 'ITEM_DB',
                'Version': 1,
            },
            'Body': items,
        }

    def convert(self, itemids, sort=False):
        items = list()
        for itemid in itemids:
            items.append(self.mapper.map_item(self.fetch_item(itemid)))
        if sort:
            items.sort(key=lambda item: item['Id'])
        return yaml.dump(self.wrap_result(items), sort_keys=False)