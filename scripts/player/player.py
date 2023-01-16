from magic import magic


class Player:
    def __init__(self):
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.lvl_point_up, self.lvl_point = 10, 0
        self.items = {}
        self.magic = list(map(lambda x: magic[x](), ['agi', 'explosion', 'dark-bolt']))
        self.exp = 0
        self.stats = {
            'attack': 2,
            'endurance': 5,
        }
        self.lvl = 1

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
