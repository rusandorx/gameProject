import os

import pygame

from combat_effects import DefenceBuff, AttackBuff
from enemies.combat_enemy import CombatEnemy
from spritesheet import SpriteSheet


class KnightEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        self.particle.offset = (25, 120)
        for i in range(lvl - 1):
            self.level_up()
        self.actions_to_methods['buff'] = self.buff
        self.actions_to_methods['debuff_attack'] = self.debuff_attack
        self.load_assets()

    def load_assets(self):
        super().load_assets()
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
                    pygame.Rect(0, 0, 128, 128), 6, (0, 0, 0)))),
            'buff': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)), SpriteSheet(os.path.join(graphics_path, 'Buff.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), 2, (0, 0, 0)))),
            'debuff_attack': list(
                map(lambda sprite: pygame.transform.chop(
                    pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    pygame.Rect(64, 512, 128, 512)), SpriteSheet(os.path.join(graphics_path, 'Attack 3.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def buff(self):
        self.add_effect(DefenceBuff({'name': 'def_up', 'turn_count': 2, 'color': (0, 64, 192), 'def_up_value': 1.2}))
        self.animate_once('buff')

    def debuff_attack(self, target=None):
        target = target if target is not None else self.player
        target.add_effect(AttackBuff({'name': 'attack_up', 'turn_count': 2, 'color': (48, 0, 0), 'attack_value': .75}))
        self.animate_once('debuff_attack')

