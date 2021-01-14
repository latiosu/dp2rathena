from enum import Enum

import copy
import re

class RAType(Enum):
    HEALING = 'Healing'             # Healing item.
    USABLE = 'Usable'               # Usable item.
    ETC = 'Etc'                     # Etc item.
    ARMOR = 'Armor'                 # Armor/Garment/Boots/Headgear/Accessory item.
    WEAPON = 'Weapon'               # Weapon item.
    CARD = 'Card'                   # Card item.
    PET_EGG = 'PetEgg'              # Pet egg item.
    PET_ARMOR = 'PetArmor'          # Pet equipment item.
    AMMO = 'Ammo'                   # Ammo (Arrows/Bullets/etc) item.
    DELAY_CONSUME = 'DelayConsume'  # Usable with delayed consumption (intended for 'itemskill').
    SHADOW_GEAR = 'ShadowGear'      # Shadow Equipment item.
    CASH = 'Cash'                   # A delayed consume requiring user confirmation on-use.

class RASubtypeWeapon(Enum):
    DAGGER = 'Dagger'
    ONE_SWORD = '1hSword'
    TWO_SWORD = '2hSword'
    ONE_SPEAR = '1hSpear'
    TWO_SPEAR = '2hSpear'
    ONE_AXE = '1hAxe'
    TWO_AXE = '2hAxe'
    ONE_MACE = 'Mace'
    TWO_MACE = '2hMace'
    ONE_STAFF = 'Staff'
    TWO_STAFF = '2hStaff'
    BOW = 'Bow'
    KNUCKLE = 'Knuckle'
    MUSICAL = 'Musical'
    WHIP = 'Whip'
    BOOK = 'Book'
    KATAR = 'Katar'
    REVOLVER = 'Revolver'
    RIFLE = 'Rifle'
    GATLING = 'Gatling'
    SHOTGUN = 'Shotgun'
    GRENADE = 'Grenade'
    HUUMA = 'Huuma'

class RASubtypeAmmo(Enum):
    ARROW = 'Arrow'
    DAGGER = 'Dagger'
    BULLET = 'Bullet'
    SHELL = 'Shell'
    GRENADE = 'Grenade'
    SHURIKEN = 'Shuriken'
    KUNAI = 'Kunai'
    CANNON_BALL = 'CannonBall'
    THROW_WEAPON = 'ThrowWeapon'

class RAJob(Enum):
    ALL = 'All'                   # Applies to all jobs listed below.
    ACOLYTE = 'Acolyte'
    ALCHEMIST = 'Alchemist'
    ARCHER = 'Archer'
    ASSASSIN = 'Assassin'
    BARDDANCER = 'BardDancer'     # Applies to Bard and Dancer.
    BARD = 'Bard'                 # Not used in rathena, for mapping tool only
    BLACKSMITH = 'Blacksmith'
    CRUSADER = 'Crusader'
    DANCER = 'Dancer'             # Not used in rathena, for mapping tool only
    GUNSLINGER = 'Gunslinger'
    HUNTER = 'Hunter'
    KAGEROUOBORO = 'KagerouOboro' # Applies to Kagerou and Oboro.
    KNIGHT = 'Knight'
    MAGE = 'Mage'
    MERCHANT = 'Merchant'
    MONK = 'Monk'
    NINJA = 'Ninja'
    NOVICE = 'Novice'
    PRIEST = 'Priest'
    REBELLION = 'Rebellion'
    ROGUE = 'Rogue'
    SAGE = 'Sage'
    SOULLINKER = 'SoulLinker'
    STARGLADIATOR = 'StarGladiator'
    SUMMONER = 'Summoner'
    SUPERNOVICE = 'SuperNovice'
    SWORDMAN = 'Swordman'
    TAEKWON = 'Taekwon'
    THIEF = 'Thief'
    WIZARD = 'Wizard'

class RAClass(Enum):
    ALL = 'All'                 # Applies to all classes.
    NORMAL = 'Normal'           # Normal classes (no Baby/Transcendent/Third classes).
    UPPER = 'Upper'             # Transcedent classes (no Transcedent-Third classes).
    BABY = 'Baby'               # Baby classes (no Third-Baby classes).
    THIRD = 'Third'             # Third classes (no Transcedent-Third or Third-Baby classes).
    THIRD_UPPER = 'Third_Upper' # Transcedent-Third classes.
    THIRD_BABY = 'Third_Baby'   # Third-Baby classes.
    ALL_UPPER = 'All_Upper'     # All Transcedent classes
    ALL_BABY = 'All_Baby'       # All baby classes
    ALL_THIRD = 'All_Third'     # Applies to all Third classes.

class RAGender(Enum):
    FEMALE = 'Female'
    MALE = 'Male'
    BOTH = 'Both'

class RALocation(Enum):
    HEAD_TOP = 'Head_Top'                             # Upper Headgear
    HEAD_MID = 'Head_Mid'                             # Middle Headgear
    HEAD_LOW = 'Head_Low'                             # Lower Headgear
    ARMOR = 'Armor'                                   # Armor
    RIGHT_HAND = 'Right_Hand'                         # Weapon
    LEFT_HAND = 'Left_Hand'                           # Shield
    GARMENT = 'Garment'                               # Garment/Robe
    SHOES = 'Shoes'                                   # Shoes
    RIGHT_ACCESSORY = 'Right_Accessory'               # Accessory Right
    LEFT_ACCESSORY = 'Left_Accessory'                 # Accessory Left
    COSTUME_HEAD_TOP = 'Costume_Head_Top'             # Costume Top Headgear
    COSTUME_HEAD_MID = 'Costume_Head_Mid'             # Costume Mid Headgear
    COSTUME_HEAD_LOW = 'Costume_Head_Low'             # Costume Low Headgear
    COSTUME_GARMENT = 'Costume_Garment'               # Costume Garment/Robe
    AMMO = 'Ammo'                                     # Ammo
    SHADOW_ARMOR = 'Shadow_Armor'                     # Shadow Armor
    SHADOW_WEAPON = 'Shadow_Weapon'                   # Shadow Weapon
    SHADOW_SHIELD = 'Shadow_Shield'                   # Shadow Shield
    SHADOW_SHOES = 'Shadow_Shoes'                     # Shadow Shoes
    SHADOW_RIGHT_ACCESSORY = 'Shadow_Right_Accessory' # Shadow Accessory Right (Earring)
    SHADOW_LEFT_ACCESSORY = 'Shadow_Left_Accessory'   # Shadow Accessory Left (Pendant)
    BOTH_HAND = 'Both_Hand'                           # Right_Hand + Left_Hand
    BOTH_ACCESSORY = 'Both_Accessory'                 # Right_Accessory + Left_Accessory

class DPType(Enum):
    HELM = 'Helm'
    ARMOR = 'Armor'
    SHIELD = 'Shield'
    GARMENT = 'Garment'
    SHOES = 'Shoes'
    ACCESSORY = 'Accessory'
    PET = 'Pet'
    COSTUME = 'Costume'                 # rathena flags costumes in 'location'
    COSTUME_HELM = 'Costume_Helm'
    COSTUME_GARMENT = 'Costume_Garment'
    COSTUME_FLOOR = 'Costume_Floor'     # Not implemented in rathena
    CONSUMABLE = 'Consumable'           # Generic category used with consumables
    SPECIAL = 'Special'                 # Another category used with consumables
    REGENERATION = 'Regeneration'       # Used for stat buffs and healing items

class Mapper:
    def __init__(self):
        self.schema = {
            'Id': 'id',                       # Item ID.
            'AegisName': 'aegisName',         # Server name to reference the item in scripts and lookups, no spaces.
            'Name': self._name,                # Name in English for displaying as output.
            'Type': self._itemTypeId,          # Item type.
            'SubType': self._itemSubTypeId,    # Weapon or Ammo type.
            'Buy': 'price',                   # Buying price. When not specified, becomes double the sell price.
            'Sell': self._sell,                # Selling price. When not specified, becomes half the buy price.
            'Weight': self._weight,            # Item weight. Each 10 is 1 weight.
            'Attack': 'attack',               # Weapon's attack.
            'MagicAttack': 'matk',            # Weapon's magic attack.
            'Defense': 'defense',             # Armor's defense.
            'Range': 'range',                 # Weapon's attack range.
            'Slots': 'slots',                 # Available slots in item.
            'Jobs': self._job,                 # Jobs that can equip the item. (Map default is 'All: true')
            'Classes': self._classes,         # Upper class types that can equip item. (Map default is 'All: true')
            'Gender': self._gender,            # Gender that can equip the item.
            'Locations': self._locationId,     # Equipment's placement.
            'WeaponLevel': self._itemLevel,    # Weapon level.
            'EquipLevelMin': 'requiredLevel', # Minimum required level to equip.
            'EquipLevelMax': 'limitLevel',    # Maximum level that can equip.
            'Refineable': 'refinable',        # If the item can be refined.
            'View': self._classNum,           # View sprite of an item.
            # 'AliasName': None,              # Another item's AegisName to be sent to client instead of this AegisName.
            # 'Flags': {                      # Item flags.
            #     'BuyingStore': None,        # If the item is available for Buyingstores.
            #     'DeadBranch': None,         # If the item is a Dead Branch.
            #     'Container': None,          # If the item is part of a container.
            #     'UniqueId': None,           # If the item is a unique stack.
            #     'BindOnEquip': None,        # If the item is bound to the character upon equipping.
            #     'DropAnnounce': None,       # If the item has a special announcement to self on drop.
            #     'NoConsume': None,          # If the item is consumed on use.
            #     'DropEffect': None,         # If the item has a special effect when on the ground.
            # },
            # 'Delay': {                      # Item use delay.
            #     'Duration': None,           # Duration of delay in seconds.
            #     'Status': None,             # Status Change used to track delay.
            # },
            # 'Stack': {                      # Item stack amount.
            #     'Amount': None,             # Maximum amount that can be stacked.
            #     'Inventory': None,          # If the stack is applied to player's inventory.
            #     'Cart': None,               # If the stack is applied to the player's cart.
            #     'Storage': None,            # If the stack is applied to the player's storage.
            #     'GuildStorage': None,       # If the stack is applied to the player's guild storage.
            # },
            # 'NoUse': {                      # Conditions when the item is unusable.
            #     'Override': None,           # Group level to override these conditions.
            #     'Sitting': None,            # If the item can not be used while sitting.
            # },
            'Trade': self._itemMoveInfo,
            # 'Script': None,                 # Script to execute when the item is used/equipped.
            # 'EquipScript': None,            # Script to execute when the item is equipped.
            # 'UnEquipScript': None,          # Script to execute when the item is unequipped or a rental item expires.
        }

        self.trade_schema = {               # Trade restrictions.
            # 'Override': None,             # Group level to override these conditions.
            'NoDrop': 'drop',               # If item cannot be dropped.
            'NoTrade': 'trade',             # If item cannot be traded.
            # 'TradePartner': None,         # If item cannot be traded to the player's partner.
            'NoSell': 'sell',               # If item cannot be sold.
            'NoCart': 'cart',               # If item cannot be put in a cart.
            'NoStorage': 'store',           # If item cannot be put in a storage.
            'NoGuildStorage': 'guildStore', # If item cannot be put in a guild storage.
            'NoMail': 'mail',               # If item cannot be put in a mail.
            'NoAuction': 'auction',         # If item cannot be put in an auction.
        }

        self.item_type_map = {
            0: None,
            1: RAType.WEAPON,
            2: RAType.ARMOR,
            3: DPType.CONSUMABLE,
            4: RAType.AMMO,
            5: RAType.ETC,
            6: RAType.CARD,
            7: RAType.CASH,
            9: DPType.COSTUME,
            10: RAType.SHADOW_GEAR
        }

        self.item_subtype_map = {
            0: None,
            256: RASubtypeWeapon.DAGGER,
            257: RASubtypeWeapon.ONE_SWORD,
            258: RASubtypeWeapon.TWO_SWORD,
            259: RASubtypeWeapon.ONE_SPEAR,
            260: RASubtypeWeapon.TWO_SPEAR,
            261: RASubtypeWeapon.ONE_AXE,
            262: RASubtypeWeapon.TWO_AXE,
            263: RASubtypeWeapon.ONE_MACE,
            264: RASubtypeWeapon.TWO_MACE,
            265: RASubtypeWeapon.ONE_STAFF,
            266: RASubtypeWeapon.TWO_STAFF,
            267: RASubtypeWeapon.BOW,
            268: RASubtypeWeapon.KNUCKLE,
            269: RASubtypeWeapon.MUSICAL,
            270: RASubtypeWeapon.WHIP,
            271: RASubtypeWeapon.BOOK,
            272: RASubtypeWeapon.KATAR,
            273: RASubtypeWeapon.REVOLVER,
            274: RASubtypeWeapon.RIFLE,
            275: RASubtypeWeapon.GATLING,
            276: RASubtypeWeapon.SHOTGUN,
            277: RASubtypeWeapon.GRENADE,
            278: RASubtypeWeapon.HUUMA,
            280: RALocation.SHADOW_WEAPON,
            512: DPType.HELM,
            513: DPType.ARMOR,
            514: DPType.SHIELD,
            515: DPType.GARMENT,
            516: DPType.SHOES,
            517: DPType.ACCESSORY,
            518: DPType.PET,
            519: DPType.COSTUME_HELM,
            522: DPType.COSTUME_GARMENT,
            525: DPType.COSTUME_FLOOR,
            526: RALocation.SHADOW_ARMOR,
            527: RALocation.SHADOW_SHIELD,
            528: RALocation.SHADOW_SHOES,
            529: RALocation.SHADOW_RIGHT_ACCESSORY,
            530: RALocation.SHADOW_LEFT_ACCESSORY,
            768: DPType.SPECIAL,
            769: DPType.REGENERATION,
            1024: RASubtypeAmmo.ARROW,
            1025: RASubtypeAmmo.CANNON_BALL,
            1026: RASubtypeAmmo.THROW_WEAPON,
            1027: RASubtypeAmmo.BULLET,
        }

        self.job_map = {
            RAJob.NOVICE:       0x00001,
            RAJob.SWORDMAN:     0x00002,
            RAJob.MAGE:         0x00004, # 83 for 3rd job
            RAJob.ARCHER:       0x00008,
            RAJob.ACOLYTE:      0x00010,
            RAJob.MERCHANT:     0x00020, # 81 for 3rd job
            RAJob.THIEF:        0x00040, # 82 for 3rd job
            RAJob.KNIGHT:       0x00080, # 95 Lord Knight, 111 Rune Knight
            RAJob.WIZARD:       0x00100, # 99 High Wizard, 118 Warlock
            RAJob.HUNTER:       0x00200, # ? Sniper, 116 Ranger
            RAJob.PRIEST:       0x00400, # 105 High Priest, 122 Arch Bishop
            RAJob.BLACKSMITH:   0x00800, # 97 Whitesmith, 115 Mechanic
            RAJob.ASSASSIN:     0x01000, # ? Assassin Cross, 114 Guillotine Cross
            RAJob.CRUSADER:     0x02000, # Paladin, 112 Royal Guard
            RAJob.SAGE:         0x04000, # ? Professor, 119 Sorceror
            RAJob.BARDDANCER:   0x08000, # Used in rathena yaml
            RAJob.BARD:         0x08000, # Not used in rathena yaml, Bard - ? Clown, 120 Minstrel
            RAJob.DANCER:       0x10000, # Not used in rathena yaml, Dancer - ? Gypsy, 121 Wanderer
            RAJob.MONK:         0x20000, # 106 Champion, 123 Sura
            RAJob.ALCHEMIST:    0x40000, # ? Biochemist, 117 Genetic
            RAJob.ROGUE:        0x80000, # 107 Stalker, 124 Shadow Chaser
            RAJob.ALL:          0xFFFFF,
        }

        # Warning: DP doesn't use composable enums for newer jobs
        self.extended_job_map = {
            73: RAJob.GUNSLINGER,
            74: RAJob.NINJA,
            141: RAJob.SOULLINKER,
            142: RAJob.SUMMONER,
            143: RAJob.TAEKWON,
            144: [RAJob.KAGEROUOBORO, RAJob.REBELLION],
            145: RAJob.STARGLADIATOR, # Star Emperor in DP but no enum for rathena
            146: RAJob.SOULLINKER,    # Soul Reaper in DP but no enum for rathena
            500: RAJob.REBELLION,
            501: RAJob.KAGEROUOBORO,
            502: RAJob.SUPERNOVICE,
            503: RAJob.STARGLADIATOR,
        }

        # TODO: Identify pattern for 'class_num' field in DP
        self.class_map = {
            0: RAClass.ALL,
            0: RAClass.NORMAL,
            0: RAClass.UPPER,
            0: RAClass.BABY,
            12: RAClass.THIRD,
            12: RAClass.THIRD_UPPER,
            12: RAClass.THIRD_BABY,
            3: RAClass.ALL_UPPER,
            0: RAClass.ALL_BABY,
            15: RAClass.ALL_THIRD,
        }

        self.location_map = {
            0x000022: RALocation.BOTH_HAND,              # DP location: null
            0x000088: RALocation.BOTH_ACCESSORY,         # DP location: null
            0x000100: RALocation.HEAD_TOP,               # DP location: Upper
            0x000200: RALocation.HEAD_MID,               # DP location: Middle
            0x000001: RALocation.HEAD_LOW,               # DP location: Lower
            0x000010: RALocation.ARMOR,                  # DP location: null
            0x000002: RALocation.RIGHT_HAND,             # DP location: null
            0x000020: RALocation.LEFT_HAND,              # DP location: null
            0x000004: RALocation.GARMENT,                # DP location: null
            0x000040: RALocation.SHOES,                  # DP location: null
            0x000008: RALocation.RIGHT_ACCESSORY,        # DP location: null
            0x000080: RALocation.LEFT_ACCESSORY,         # DP location: null
            0x000400: RALocation.COSTUME_HEAD_TOP,       # DP location: Upper
            0x000800: RALocation.COSTUME_HEAD_MID,       # DP location: Middle
            0x001000: RALocation.COSTUME_HEAD_LOW,       # DP location: Lower
            0x002000: RALocation.COSTUME_GARMENT,        # DP location: Garment
            # 0x000000: RALocation.AMMO,                 # Not a DP location, use RAType.AMMO instead
            0x010000: RALocation.SHADOW_ARMOR,           # DP location: Armor
            0x020000: RALocation.SHADOW_WEAPON,          # DP location: null
            0x040000: RALocation.SHADOW_SHIELD,          # DP location: Shield
            0x080000: RALocation.SHADOW_SHOES,           # DP location: Shoes
            0x100000: RALocation.SHADOW_RIGHT_ACCESSORY, # DP location: Accessory
            0x200000: RALocation.SHADOW_LEFT_ACCESSORY,  # DP location: Accessory
        }

    def _validate(self, data, *argv):
        for arg in argv:
            assert arg in data
            v = data[arg]
            msg = f'Unrecognised {arg}: {v}'
            if arg == 'itemTypeId':
                assert v in self.item_type_map, msg
            elif arg == 'itemSubTypeId':
                assert v in self.item_subtype_map, msg
            elif arg == 'locationId' and v is not None:
                assert v >= 0 and v <= 0x3FFFFF, msg
            elif arg == 'job' and v is not None:
                assert v >= 0 and v <= 0xFFFFF, msg
            elif arg == 'itemLevel' and v is not None:
                assert v >= 0 and v <= 4, msg
            elif arg == 'classNum' and v is not None:
                assert v >= 0, msg

    def _name(self, data):
        self._validate(data, 'name')
        if data['name'] is None:
            return ''
        return re.sub(r'\s\[[1-9]\]$', '', data['name'])

    def _itemTypeId(self, data):
        self._validate(data, 'itemTypeId', 'itemSubTypeId')
        itemType = self.item_type_map[data['itemTypeId']]
        itemSubType = self.item_subtype_map[data['itemSubTypeId']]

        # Warning: DP doesn't separate Pet Armor from Pet Eggs so we use "Egg"
        # in name as a heuristic
        if itemSubType == DPType.PET and itemType == RAType.ARMOR:
            if 'Egg' in data['name']:
                return RAType.PET_EGG.value
            else:
                return RAType.PET_ARMOR.value

        # Warning: Consumables are not handled consistently in DP so we let
        # user choose correct option
        if itemType == DPType.CONSUMABLE:
            if itemSubType == DPType.REGENERATION:
                return RAType.HEALING.value
            elif itemSubType == DPType.SPECIAL:
                options = [RAType.HEALING, RAType.USABLE, RAType.DELAY_CONSUME, RAType.CASH]
                return '/'.join(map(lambda v : v.value, options))

        if itemType == DPType.COSTUME:
            return RAType.ARMOR.value
        return None if itemType is None else itemType.value

    def _itemSubTypeId(self, data):
        self._validate(data, 'itemTypeId', 'itemSubTypeId')
        itemType = self.item_type_map[data['itemTypeId']]
        itemSubType = self.item_subtype_map[data['itemSubTypeId']]

        # Warning: DP maps subset of RA values, let user choose correct option
        if itemType == RAType.AMMO:
            return '/'.join(map(lambda v : v.value, RASubtypeAmmo))

        if itemType == RAType.WEAPON:
            return None if itemSubType is None else itemSubType.value
        return None

    def _sell(self, data):
        # Note: This value is currently omitted in rathena YAML by default
        return None

    def _weight(self, data):
        self._validate(data, 'weight')
        w = data['weight']
        if w < 0:
            return 0
        return int(w * 10)

    def _job(self, data):
        self._validate(data, 'job')
        job_id = data['job']
        if job_id is None or job_id == 0:
            return None

        jobs = dict()
        # Warning: DP API doesn't combine 1st and 2nd jobs with other jobs so
        # items which are usable by both can't be determined. Eg. Knife (1201)
        if job_id in self.extended_job_map:
            mapping = self.extended_job_map[job_id]
            if type(mapping) is list:
                for v in mapping:
                    jobs[v.value] = True
            else:
                jobs[mapping.value] = True
        else:
            if job_id & 0xFFFFF == 0xFFFFF:
                return None
            for k, v in self.job_map.items():
                if job_id & v == v:
                    # Note: rathena groups Novice and Supernovice permissions
                    if k == RAJob.NOVICE:
                        jobs[RAJob.SUPERNOVICE.value] = True
                    jobs[k.value] = True

        # Result is sorted alphabetically in rathena
        return dict(sorted(jobs.items()))

    def _classes(self, data):
        # Note: This value isn't clearly defined by DP, will revisit when more
        # information is available
        return None

    def _gender(self, data):
        self._validate(data, 'job')
        job_id = data['job']
        if job_id is None or job_id == 0:
            return None

        bard_id = self.job_map[RAJob.BARD]
        dancer_id = self.job_map[RAJob.DANCER]
        if job_id & self.job_map[RAJob.ALL] == self.job_map[RAJob.ALL]:
            return None
        elif job_id & (bard_id + dancer_id) == (bard_id + dancer_id):
            return RAGender.BOTH.value
        elif job_id & bard_id == bard_id:
            return RAGender.MALE.value
        elif job_id & dancer_id == dancer_id:
            return RAGender.FEMALE.value
        else:
            return None

    def _locationId(self, data):
        self._validate(data, 'locationId', 'itemTypeId')
        location_id = data['locationId']
        locs = dict()
        if location_id is None or location_id == 0:
            # DP doesn't have Ammo location so we handle separately
            if self.item_type_map[data['itemTypeId']] == RAType.AMMO:
                locs[RALocation.AMMO.value] = True
            else:
                return None

        for k, v in self.location_map.items():
            if location_id & k == k:
                locs[self.location_map[k].value] = True

        # Clean up 'both' locations
        if RALocation.LEFT_HAND.value in locs and RALocation.RIGHT_HAND.value in locs:
            del locs[RALocation.LEFT_HAND.value]
            del locs[RALocation.RIGHT_HAND.value]
        if RALocation.LEFT_ACCESSORY.value in locs and RALocation.RIGHT_ACCESSORY.value in locs:
            del locs[RALocation.LEFT_ACCESSORY.value]
            del locs[RALocation.RIGHT_ACCESSORY.value]
        return locs

    def _itemLevel(self, data):
        self._validate(data, 'itemLevel')
        if data['itemLevel'] == 0:
            return None
        return data['itemLevel']

    def _classNum(self, data):
        self._validate(data, 'classNum')
        if data['classNum'] == 0:
            return None
        return data['classNum']

    def _itemMoveInfo(self, data):
        self._validate(data, 'itemMoveInfo')
        result = self._map_schema(copy.copy(self.trade_schema), data['itemMoveInfo'])
        cleaned = {'Override': 100} # rathena outputs 100 by default

        # Note: rathena excludes this section when no trade restrictions exist
        exclude = True
        for k, v in self.trade_schema.items():
            # DP uses positive notion of trade but rathena uses negation notion
            if k not in result:
                exclude = False
                cleaned[k] = True

        if exclude:
            return None
        return cleaned

    def _map_schema(self, schema, data):
        if schema is None:
            return None
        elif data is None:
            return schema
        result = copy.deepcopy(schema)
        for k, v in schema.items():
            if v is None:
                del result[k]
            elif callable(v):
                if v(data) == None:
                    del result[k]
                else:
                    result[k] = v(data)
            elif type(v) is dict:
                result[k] = self._map_schema(v, data)
            elif type(v) is str or type(v) is int:
                if v not in data or data[v] == 0 or data[v] == None:
                    del result[k]
                else:
                    result[k] = data[v]
            else:
                result[k] = v
        return result

    def map_item(self, data):
        if data is None or 'Error' in data:
            return data
        return self._map_schema(self.schema, data)
