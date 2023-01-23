from item import items
from magic import magic


class Player:
    def __init__(self):
        with open("../data/player.txt") as data:
            self.data = data.read().split("\n")
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.lvl_point_up, self.lvl_point = 10, 0
        self.items = {items[name]: items[name].count for name in
                      ('small_potion', 'medium_potion', 'small_mana_potion', 'molotov')}
        self.magic = list(map(lambda x: magic[x](), ['agi']))
        self.exp = 0
        self.stats = {
            'attack': 7,
            'endurance': 5,
            'weaknesses': []
        }
        self.lvl = 1
        for i in range(int(self.data[0].split()[1]) - 1):
            self.level_up()

    def level_up(self):
        self.lvl_point -= self.lvl_point_up
        self.lvl_point_up *= 1.05
        self.max_hp *= 1.05
        self.max_mp *= 1.05
        self.lvl += 1
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.stats["endurance"] += 1
        self.stats["attack"] *= 1.05
        new_magic = MAGIC_MAP.get(self.lvl, None)
        if new_magic is not None:
            self.magic.append(magic[new_magic]())

        new_items = ITEMS_MAP.get(self.lvl, None)
        if new_items is not None:
            if items[new_items] not in self.items:
                self.items[items[new_items]] = items[new_items].count
            else:
                items[new_items].count += 1
                self.items[items[new_items]] = items[new_items].count

    def use_item(self, item):
        self.items[item] -= 1
        if self.items[item] <= 0:
            del self.items[item]
            item.count = 0
            return
        item.count = self.items[item]

    def add_item(self, item):
        if item not in self.items:
            self.items[item] = 0
        self.items[item] += 1
        item.count = self.items[item]


MAGIC_MAP = {
    2: 'dark-bolt',
    4: 'heal',
    7: 'lightning',
    8: 'shield',
    10: 'explosion'
}

ITEMS_MAP = {
    2: 'small_potion',
    6: 'molotov',
    8: 'small_mana_potion',
    10: 'small_potion'
}
