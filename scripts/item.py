import os
from abc import ABC, abstractmethod

import pygame

from combat_effects import BurnEffect
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

    @abstractmethod
    def can_be_used(self, player: CombatPlayer):
        pass


class HealthPotionItem(Item):
    def __init__(self, options: dict):
        super().__init__(options)
        self.heal_hp = options['heal_hp']

    def use(self, player: CombatPlayer, target: CombatEnemy):
        super().use(player, target)
        player.player.hp = min(player.player.hp + self.heal_hp, player.player.max_hp)

    def can_be_used(self, player):
        return player.hp < player.max_hp


class ManaPotionItem(Item):
    def __init__(self, options: dict):
        super().__init__(options)
        self.heal_mp = options['heal_mp']

    def use(self, player: CombatPlayer, target: CombatEnemy):
        super().use(player, target)
        player.player.mp = min(player.player.mp + self.heal_mp, player.player.max_mp)

    def can_be_used(self, player):
        return player.mp < player.max_mp


class MolotovItem(Item):
    def __init__(self, options: dict):
        super().__init__(options)

    def use(self, player: CombatPlayer, target: CombatEnemy):
        super().use(player, target)
        target.add_effect(BurnEffect({'name': 'burn', 'turn_count': 3, 'color': (192, 64, 0), 'damage': 2}))

    def can_be_used(self, player: CombatPlayer):
        return True


items = {
    'small_potion': HealthPotionItem({
        'name': 'Small potion',
        'description': 'Зелье... В пузырьке осталось немного.',
        'heal_hp': 15
    }),
    'medium_potion': HealthPotionItem({
        'name': 'Medium potion',
        'description': 'Этого зелья хватит чтобы ненадолго перекрыть боль.',
        'heal_hp': 30
    }),
    'small_mana_potion': ManaPotionItem({
        'name': 'Small mana potion',
        'description': 'Скудно восстанавливает ману.',
        'heal_mp': 15
    }),
    'molotov': MolotovItem({
        'name': 'Molotov',
        'description': 'Поджигает врага на 3 хода.',
        'damage_per_turn': 5,
        'need_target': True
    })
}
