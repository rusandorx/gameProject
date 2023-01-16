from magic import magic


class Player:
    def __init__(self):
        self.max_hp, self.hp = 100, 100
        self.max_mp, self.mp = 50, 50
        self.items = {}
        self.magic = list(map(lambda x: magic[x](), ['agi', 'explosion', 'dark-bolt']))
        self.exp = 0
        self.stats = {
            'attack': 10,
            'endurance': 5,
        }
        self.lvl = 1