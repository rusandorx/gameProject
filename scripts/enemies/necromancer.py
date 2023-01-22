import os

import pygame

from enemies.combat_enemy import CombatEnemy
from spritesheet import SpriteSheet


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
        super().load_assets()
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
