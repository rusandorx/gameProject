import os

import pygame.sprite

from EffectsParticle import EffectsParticle
from entity import Entity
from spritesheet import SpriteSheet


class CombatPlayer(Entity):
    def __init__(self, position, player, *groups):
        super().__init__(*groups)
        self.position = position
        self.player = player
        self.stats = self.player.stats

        self.on_animation_end = []
        self.effects = {}
        self.on_turn_end = []

        self.load_assets()

    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/player/'
        self.sprites = {
            'idle': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                             SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                                 pygame.Rect(0, 0, 128, 128), 7, (0, 0, 0)))),
            'attack': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                               SpriteSheet(os.path.join(graphics_path, 'Attack_1.png')).load_strip(
                                   pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
            'hurt': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                             SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                                 pygame.Rect(0, 0, 128, 128), 3, (0, 0, 0)))),
            'die': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                            SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                                pygame.Rect(0, 0, 128, 128), 6, (0, 0, 0))))
        }
        for magic in self.player.magic:
            if magic.damage_type == 'physical':
                self.sprites[f'{magic.damage_type}-magic'] = self.sprites['attack']
                continue
            if magic.damage_type == 'heal' or magic.damage_type == 'buff':
                self.sprites[f'{magic.damage_type}-magic'] = list(
                    map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                        SpriteSheet(os.path.join(graphics_path, f'{magic.damage_type}-magic.png')).load_strip(
                            pygame.Rect(0, 0, 128, 128), 8, (0, 0, 0))))
                continue
            self.sprites[f'{magic.damage_type}-magic'] = list(
                map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                    SpriteSheet(os.path.join(graphics_path, f'{magic.damage_type}-magic.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 14, (0, 0, 0))))
        self.sprite_state = 'idle'
        self.return_to_idle = False
        self.animation_frame = 0
        self.animation_speed = .1

        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.particle = EffectsParticle(self, (-100, 100), 100, 120)

    def update(self):
        self.animate()

    def take_damage(self, damage, damage_type="physical"):
        if damage_type != "physical":
            self.player.hp -= damage * 0.95
        else:
            self.player.hp -= damage * 0.95 ** self.player.stats['endurance']
        self.animate_once('hurt')
        if self.player.hp <= 0:
            self.animate_to_last_frame('die')
            with open("../data/player.txt", "w") as data:
                data.write(f"lvl {1}")

    def return_object_to_apply(self):
        return self.player
