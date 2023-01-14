from abc import ABC, abstractmethod, ABCMeta
from random import choices, randint

import pygame


class CombatEnemy(pygame.sprite.Sprite, metaclass=ABCMeta):
    '''
    stats: {
        "strength": int,
        "endurance": int,
        "type": [Types],
        "weaknesses" [Types],
        "actions": {
            attack: .4,
            magic: .2,
            ...
        }
    }
    '''

    def __init__(self, name, lvl, hp, stats, position, *groups):
        super().__init__(*groups)
        self.name = name
        self.max_hp = hp * (lvl * .05)
        self.hp = self.max_hp
        self.lvl = lvl
        self.stats = stats
        self.position = position

        self.sprites = []
        self.actions_to_methods = {
            'attack': self.attack,
            'magic': self.magic
        }
        self.actions = self.stats['actions']
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.animation_speed = .1
        self.return_to_idle = False
        self.stop_at_last_frame = False
        self.active = True

    def animate_once(self, animation_state):
        self.animation_state = animation_state
        self.return_to_idle = True

    def animate_to_last_frame(self, animate_state):
        self.animation_state = animate_state
        self.return_to_idle = False
        self.stop_at_last_frame = True

    @abstractmethod
    def load_assets(self):
        pass

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(sprites):
            self.animation_frame = 0
            if self.return_to_idle:
                self.return_to_idle = False
                self.sprite_state = 'idle'
                return

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def attack(self):
        self.animate_once('attack')
        return self.stats['attack'] * (self.lvl / 10), self.stats['type']

    def magic(self):
        # TODO: Magic
        self.attack()

    def take_damage(self, damage, damage_type):
        self.hp -= (damage * (1 - self.stats['endurance'] * 0.01)) \
                   * (1.5 if any(stat == damage_type for stat in self.stats['type']) else 1)
        if self.hp <= 0:
            return self.die()

        self.animate_once('hurt')

    def die(self):
        self.active = False

    def update(self):
        self.animate()

    def random_action(self):
        self.actions_to_methods[choices(self.actions, weights=[action for action in self.actions])]()


class SkeletonEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position):
        super().__init__(name, lvl, hp, stats, position)


enemies = {
    'skeleton': lambda position: SkeletonEnemy('skeleton', randint(1, 5), 30, {
        'attack': 5,
        'endurance': 3,
        'weaknesses': ['light'],
        'type': ['dark'],
        'actions': {
            'attack': .7,
            'magic': .3
        },
    }, position),
    'green_boss': lambda position: SkeletonEnemy('green_boss', randint(20, 30), 100, {
        'attack': 20,
        'endurance': 100,
        'weaknesses': [],
        'type': ['god'],
        'actions': {
            'attack': .95,
            'magic': .05
        },
    }, position)
}
