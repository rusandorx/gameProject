import os
from random import choices

import pygame

from combat_effects import BleedingEffect
from enemies.combat_enemy import CombatEnemy
from spritesheet import SpriteSheet


class SkeletonEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        self.particle.offset = (-15, 110)
        for i in range(lvl - 1):
            self.level_up()
        self.load_assets()
        self.actions_to_methods['strong_attack'] = self.strong_attack
        self.actions_to_methods['bleeding_attack'] = self.bleeding_attack

    def load_assets(self):
        super().load_assets()

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
                        pygame.Rect(0, 0, 128, 128), 5, (0, 0, 0)))),
            'strong_attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack_1.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 5, (0, 0, 0)))),
            'bleeding_attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack_2.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def strong_attack(self, target=None):
        if target is None:
            target = self.player
        self.animate_once('strong_attack')
        target.take_damage(self.stats['attack'] * 1.5, 'physical')

    def bleeding_attack(self, target=None):
        if target is None:
            target = self.player
        is_bleeding = choices((True, False), weights=(.75, .25))[0]
        target.take_damage(self.stats['attack'] * .8, 'physical')
        self.animate_once('bleeding_attack')
        if is_bleeding:
            target.add_effect(
                BleedingEffect({'name': 'bleeding', 'turn_count': 1, 'color': (255, 0, 0), 'bleeding_value': .05}))
