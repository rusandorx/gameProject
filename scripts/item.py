import os
from abc import ABC, abstractmethod

import pygame

from enemies import CombatEnemy
from player.combat_player import CombatPlayer


class Item(ABC):
    def __init__(self, options: dict):
        self.name = options.get('name', 'Предмет')
        self.description = options.get('description', 'Описание')
        self.need_target = options.get('need_target', False)
        self.options = options
        self.count = 2
        self.load_assets()

    def load_assets(self):
        path = f'../graphics/ui/combat/items/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, self.name + '.png')), (64, 64))

    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.player.use_item(self)


class PotionItem(Item):
    def __init__(self, options: dict):
        super().__init__(options)
        self.heal_hp = options['heal_hp']

    def use(self, player: CombatPlayer, target: CombatEnemy):
        super().use(player, target)
        player.player.hp = min(player.player.hp + self.heal_hp, player.player.max_hp)

items = {
    'small_potion': PotionItem({
        'name': 'Small potion',
        'description': 'Зелье... В пузырьке осталось немного.',
        'heal_hp': 15
    }),
    'medium_potion': PotionItem({
        'name': 'Medium potion',
        'description': 'Этого зелья хватит чтобы ненадолго перекрыть боль.',
        'heal_hp': 30
    })
}
