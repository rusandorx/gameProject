import os
import random

import pygame

from enemies.combat_enemy import CombatEnemy
from spritesheet import SpriteSheet


class ZombieEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        self.particle.offset = (-15, 110)
        for i in range(lvl - 1):
            self.level_up()
        self.load_assets()
        self.actions_to_methods['heal'] = self.heal

    def load_assets(self):
        super().load_assets()

        graphics_path = '../graphics/ui/combat/sprites/Zombie/'
        attack_name = random.choice(('Attack_1', 'Attack_2', 'Attack_3'))
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                        pygame.Rect(0, 0, 96, 96), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, f'{attack_name}.png')).load_strip(
                        pygame.Rect(0, 0, 96, 96), 3, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 96, 96), 2, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                        pygame.Rect(0, 0, 96, 96), 5, (0, 0, 0)))),
            'heal': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Eating.png')).load_strip(
                        pygame.Rect(0, 0, 96, 96), 5, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def heal(self):
        if self.hp >= self.max_hp * .5:
            self.attack()
            return

        self.hp = min(self.hp + self.max_hp * .1, self.max_hp)
        self.animate_once('heal')
