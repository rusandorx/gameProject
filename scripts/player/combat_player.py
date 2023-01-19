import os

import pygame.sprite
import zope

from EffectsParticle import EffectsParticle
from combat_effects import Effect, IEffectAppliable
from entity import Entity
from spritesheet import SpriteSheet


@zope.interface.implementer(IEffectAppliable)
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
                        pygame.Rect(0, 0, 128, 128), 15, (0, 0, 0))))
        self.sprite_state = 'idle'
        self.return_to_idle = False
        self.animation_frame = 0
        self.animation_speed = .1

        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.particle = EffectsParticle(self, (-100, 100), 100, 120)

    def attack(self, target):
        self.animate_once('attack')
        target.take_damage(self.player.stats['attack'], 'physical')

    def animate_once(self, animation):
        self.animation_frame = 0
        self.sprite_state = animation
        self.return_to_idle = True

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(sprites):
            self.animation_frame = 0
            if self.return_to_idle:
                self.animation_ended()
                self.return_to_idle = False
                self.sprite_state = 'idle'
                return
        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.animate()

    def take_damage(self, damage, damage_type):
        self.player.hp -= damage * 0.95 ** self.player.stats['endurance']
        self.animate_once('hurt')
        if self.player.hp <= 0:
            self.animate_once('die')

    def animation_ended(self):
        for cb in self.on_animation_end:
            cb()
        self.on_animation_end.clear()

    def return_object_to_apply(self):
        return self.player
