import os

import pygame.sprite

from spritesheet import SpriteSheet


class CombatPlayer(pygame.sprite.Sprite):
    def __init__(self, position, player, *groups):
        super().__init__(*groups)
        self.position = position
        self.load_sprites()
        self.player = player

    def load_sprites(self):
        graphics_path = '../graphics/ui/combat/sprites/player/'
        self.sprites = {
            'idle': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                             SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                                 pygame.Rect(0, 0, 128, 128), 7, (0, 0, 0)))),
            'attack': list(map(lambda sprite: pygame.transform.scale(sprite, (512, 512)),
                               SpriteSheet(os.path.join(graphics_path, 'Attack_1.png')).load_strip(
                                   pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
        }
        self.sprite_state = 'idle'
        self.return_to_idle = False
        self.animation_frame = 0
        self.animation_speed = .1

        self.image = self.sprites['idle'][0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])

    def attack(self):
        self.set_sprite_state_once('attack')
        return self.player.stats['attack'] * (self.player.lvl / 10), 'physical'

    def set_sprite_state_once(self, sprite_state):
        self.sprite_state = sprite_state
        self.return_to_idle = True

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

    def update(self):
        self.animate()
