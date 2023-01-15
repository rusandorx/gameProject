import os
from abc import abstractmethod, ABCMeta
from random import choices, randint

import pygame

from spritesheet import SpriteSheet
from utils import get_outline


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

    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(*groups)
        self.player = player
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
        self.sprite_state = 'idle'
        self.animation_frame = 0
        self.animation_speed = .1
        self.return_to_idle = False
        self.stop_at_last_frame = False
        self.active = True
        self.outstroked = False
        self.load_assets()

    def animate_once(self, sprite_state):
        self.sprite_state = sprite_state
        self.animation_frame = 0
        self.return_to_idle = True

    def animate_to_last_frame(self, animate_state):
        self.sprite_state = animate_state
        self.animation_frame = 0
        self.return_to_idle = False
        self.stop_at_last_frame = True

    @abstractmethod
    def load_assets(self):
        pass

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        if self.stop_at_last_frame and int(self.animation_frame) >= len(sprites) - 1:
            return

        self.animation_frame += self.animation_speed * 0.5
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
        self.player.take_damage(self.stats['attack'] * (self.lvl / 10), self.stats['type'], 'physical')

    def magic(self):
        # TODO: Magic
        self.attack()

    def take_damage(self, damage, damage_type):
        if damage_type == 'physical':
            self.hp -= damage * (1 - self.stats['endurance'] * 0.01)
        else:
            self.hp -= damage * (1.5 if any(stat == damage_type for stat in self.stats['type']) else 1)
        if self.hp <= 0:
            return self.die()

        self.animate_once('hurt')

    def die(self):
        self.animate_to_last_frame('die')
        self.active = False

    def update(self):
        self.animate()

    def random_action(self):
        self.actions_to_methods[choices(self.actions, weights=[action for action in self.actions])]()


class SkeletonEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)

    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/skeleton/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack_1.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 5, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 2, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 5, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position


enemies = {
    'skeleton': lambda position, player: SkeletonEnemy('skeleton', randint(1, 5), 30, {
        'attack': 5,
        'endurance': 3,
        'weaknesses': ['light'],
        'type': ['dark'],
        'actions': {
            'attack': .7,
            'magic': .3
        },
    }, position, player),
    'green_boss': lambda position, player: SkeletonEnemy('green_boss', randint(20, 30), 100, {
        'attack': 20,
        'endurance': 50,
        'weaknesses': [],
        'type': ['god'],
        'actions': {
            'attack': .95,
            'magic': .05
        },
    }, position, player)
}
