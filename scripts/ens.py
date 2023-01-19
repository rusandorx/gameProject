import os
from random import randint

import pygame

from enemies.combat_enemy import CombatEnemy
from spritesheet import SpriteSheet


class SkeletonEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        for i in range(lvl - 1):
            self.level_up()
        self.load_assets()


    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/skeleton/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack_3.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 3, (0, 0, 0)))),
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

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


class NecromancerEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.animation_speed = 0.3
        self.stats["attack"] *= lvl
        self.boss = True
        for i in range(lvl - 1):
            self.level_up()
        self.load_assets()


    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/necromancer/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind_Idle.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 7, (0, 0, 0)) +
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Taunt.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 17, (0, 0, 0)) +
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Idle1.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Attack.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 13, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 5, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Dead.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 9, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


class KnightEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        for i in range(lvl - 1):
            self.level_up()
        self.load_assets()


    def load_assets(self):
        if self.lvl <= 10:
            graphics_path = '../graphics/ui/combat/sprites/Knight_1/'
        elif self.lvl <= 15:
            graphics_path = '../graphics/ui/combat/sprites/Knight_2/'
        else:
            graphics_path = '../graphics/ui/combat/sprites/Knight_3/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)), SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)),
                    SpriteSheet(os.path.join(graphics_path, 'Attack 2.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)), SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), 2, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)), SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), 6, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


enemies = {
    'skeleton': lambda position, player: SkeletonEnemy('skeleton', randint(1, 5), 30, {
        'attack': 0.8,
        'endurance': 10,
        'weaknesses': ['light'],
        'type': ['dark'],
        'xp': 5,
        'actions': {
            'attack': .7,
            'magic': .3,
        },
    }, position, player),
    'necromancer': lambda position, player: NecromancerEnemy('necromancer', randint(20, 30), 100, {
        'attack': 2,
        'endurance': 50,
        'weaknesses': [],
        'type': ['light'],
        'xp': 50,
        'actions': {
            'attack': .95,
            'magic': .05,
        },
    }, position, player),
    'knight': lambda position, player: KnightEnemy('knight', randint(5, 20), 30, {
        'attack': 2,
        'endurance': 10,
        'weaknesses': [],
        'type': ['light'],
        'xp': 7,
        'actions': {
            'attack': .7,
            'magic': .3,
        },
    }, position, player)
}
