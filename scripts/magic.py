from abc import ABC, abstractmethod


class Magic:
    def __init__(self, name, description, damage, damage_type, cost, folder, sprites_count):
        self.name = name
        self.description = description
        self.damage = damage
        self.damage_type = damage_type
        self.cost = cost

    def load_assets(self):



magic = {
    'agi': lambda: Magic('agi', 'Маленький огненный урон', 15, 'fire', 5, )
}
