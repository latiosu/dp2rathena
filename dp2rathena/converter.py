import io
import os
import copy
import tortilla
import json
import yaml

class Converter:
    def __init__(self):
        self.api = tortilla.wrap('https://divine-pride.net/api/database', debug=True)
        self.api.config.params.apiKey = os.getenv('DIVINEPRIDE_API_KEY')

    def fetch_item_api(self, itemid):
        return json.loads(self.api.item.get(itemid))

    def to_item_yml(self, data):
        item_mapper = Mapper()
        item = item_mapper.map_data_to_schema(data)
        return yaml.dump(item, sort_keys=False)

    def convert(self, itemid):
        return self.to_item_yml(self.fetch_item_api(itemid))

class Mapper:
    def __init__(self):
        self.schema = {
            'Id': 'id',                         # Item ID.
            'AegisName': 'aegisName',           # Server name to reference the item in scripts and lookups, should use no spaces.
            'Name': 'name',                     # Name in English for displaying as output.
            'Type': 'itemTypeId',               # Item type.
            'SubType': 'itemSubTypeId',         # Weapon or Ammo type.
            'Buy': 'price',                     # Buying price. When not specified, becomes double the sell price.
            'Sell': self.sell,                  # Selling price. When not specified, becomes half the buy price.
            'Weight': 'weight',                 # Item weight. Each 10 is 1 weight.
            'Attack': 'attack',                 # Weapon's attack.
            'MagicAttack': 'matk',              # Weapon's magic attack.
            'Defense': 'defense',               # Armor's defense.
            'Range': 'range',                   # Weapon's attack range.
            'Slots': 'slots',                   # Available slots in item.
            'Jobs': self.job,                   # Jobs that can equip the item. (Map default is 'All: true')
            'Classes': self.classNum,           # Upper class types that can equip the item. (Map default is 'All: true')
            'Gender': self.gender,              # Gender that can equip the item.
            'Locations': self.locationId,       # Equipment's placement.
            'WeaponLevel': 'itemLevel',         # Weapon level.
            'EquipLevelMin': 'requiredLevel',   # Minimum required level to equip.
            'EquipLevelMax': 'limitLevel',      # Maximum level that can equip.
            'Refineable': 'refinable',          # If the item can be refined.
            # 'View': None,                       # View sprite of an item.
            # 'AliasName': None,                  # Another item's AegisName that will be sent to the client instead of this item's AegisName.
            # 'Flags': {                          # Item flags.
            #     'BuyingStore': None,            # If the item is available for Buyingstores.
            #     'DeadBranch': None,             # If the item is a Dead Branch.
            #     'Container': None,              # If the item is part of a container.
            #     'UniqueId': None,               # If the item is a unique stack.
            #     'BindOnEquip': None,            # If the item is bound to the character upon equipping.
            #     'DropAnnounce': None,           # If the item has a special announcement to self on drop.
            #     'NoConsume': None,              # If the item is consumed on use.
            #     'DropEffect': None,             # If the item has a special effect when on the ground.
            # },
            # 'Delay': {                          # Item use delay.
            #     'Duration': None,               # Duration of delay in seconds.
            #     'Status': None,                 # Status Change used to track delay.
            # },
            # 'Stack': {                          # Item stack amount.
            #     'Amount': None,                 # Maximum amount that can be stacked.
            #     'Inventory': None,              # If the stack is applied to player's inventory.
            #     'Cart': None,                   # If the stack is applied to the player's cart.
            #     'Storage': None,                # If the stack is applied to the player's storage.
            #     'GuildStorage': None,           # If the stack is applied to the player's guild storage.
            # },
            # 'NoUse': {                          # Conditions when the item is unusable.
            #     'Override': None,               # Group level to override these conditions.
            #     'Sitting': None,                # If the item can not be used while sitting.
            # },
            'Trade': self.itemMoveInfo,
            # 'Script': None,                     # Script to execute when the item is used/equipped.
            # 'EquipScript': None,                # Script to execute when the item is equipped.
            # 'UnEquipScript': None,              # Script to execute when the item is unequipped or when a rental item expires.
        }

        self.trade_schema = {   # Trade restrictions.
            # 'Override': None,               # Group level to override these conditions.
            'NoDrop': 'drop',               # If the item can not be dropped.
            'NoTrade': 'trade',             # If the item can not be traded.
            # 'TradePartner': None,           # If the item can not be traded to the player's partner.
            'NoSell': 'sell',               # If the item can not be sold.
            'NoCart': 'cart',               # If the item can not be put in a cart.
            'NoStorage': 'store',           # If the item can not be put in a storage.
            'NoGuildStorage': 'guildStore', # If the item can not be put in a guild storage.
            'NoMail': 'mail',               # If the item can not be put in a mail.
            'NoAuction': 'auction',         # If the item can not be put in an auction.
        }

    def sell(self, data):
        return data['price'] / 2

    def job(self, data):
        return None

    def classNum(self, data):
        return None

    def gender(self, data):
        return None

    def locationId(self, data):
        return None

    def itemMoveInfo(self, data):
        trade_schema_copy = copy.copy(self.trade_schema)
        return self.map_schema(trade_schema_copy, data['itemMoveInfo'])

    def map_schema(self, schema, data):
        for k, v in schema.items():
            if v is None:
                continue
            elif type(v) is str:
                schema[k] = data[v]
            elif callable(v):
                schema[k] = v(data)
            elif type(v) is dict:
                self.map_schema(v, data)
        return schema

    def wrap_result(self, item):
        return {
            'Header': {
                'Type': 'ITEM_DB',
                'Version': 1,
            },
            'Body': [item],
        }

    def map_data_to_schema(self, data):
        schema_copy = copy.deepcopy(self.schema)
        return self.wrap_result(self.map_schema(schema_copy, data))
