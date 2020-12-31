import importlib
import json
import os

import tortilla
import yaml

from dp2rathena import item_mapper

class Converter:
    def __init__(self):
        self.api = tortilla.wrap('https://divine-pride.net/api/database', debug=True)
        self.api.config.params.apiKey = os.getenv('DIVINEPRIDE_API_KEY')

    def fetch_item_api(self, itemid):
        return self.api.item.get(itemid)

    def to_item_yml(self, data):
        mapper = item_mapper.Mapper()
        item = mapper.map_data_to_schema(data)
        return yaml.dump(item, sort_keys=False)

    def convert(self, itemid):
        return self.to_item_yml(self.fetch_item_api(itemid))