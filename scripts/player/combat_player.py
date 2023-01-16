import os

import pygame.sprite

from enemies import CombatEnemy
from spritesheet import SpriteSheet


class CombatPlayer(pygame.sprite.Sprite):
    def __init__(self, position, player, *groups):
        super().__init__(*groups)
        self.position = position
        self.load_sprites()
        self.player = player
        self.on_animation_end = []

    def load_sprites(self):
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
            'magic': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                             SpriteSheet(os.path.join(graphics_path, 'Flame_jet.png')).load_strip(
                                 pygame.Rect(0, 0, 128, 128), 3, (0, 0, 0)))),
            'die': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                             SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                                 pygame.Rect(0, 0, 128, 128), 6, (0, 0, 0))))
        }
        self.sprite_state = 'idle'
        self.return_to_idle = False
        self.animation_frame = 0
        self.animation_speed = .1

        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])

    def attack(self, target):
        self.set_sprite_state_once('attack')
        target.take_damage(self.player.stats['attack'], 'physical')

    def set_sprite_state_once(self, sprite_state):
        self.animation_frame = 0
        self.sprite_state = sprite_state
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
        self.set_sprite_state_once('hurt')
        if self.player.hp <= 0:
            self.set_sprite_state_once('die')

    def animation_ended(self):
        for cb in self.on_animation_end:
            cb()
        self.on_animation_end.clear()

