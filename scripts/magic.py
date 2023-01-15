import os

import pygame

from spritesheet import SpriteSheet


class Magic(pygame.sprite.Sprite):
    def __init__(self, name, description, damage, damage_type, cost, sprites_count, *groups):
        super().__init__(*groups)
        self.name = name
        self.description = description
        self.damage = damage
        self.damage_type = damage_type
        self.cost = cost
        self.sprites_count = sprites_count
        self.load_assets()
        self.animating = False
        self.animation_speed = .2
        self.animation_frame = 0
        self.pos = (0, 0)

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = list(
            map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (256, 256)), True, False),
                SpriteSheet(os.path.join(path, f'sprites.png')).load_strip(
                    pygame.Rect(0, 0, 256, 256), self.sprites_count, (0, 0, 0))))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()

    def update(self):
        if self.animating:
            self.animate()

    def animate(self):
        sprites = self.sprites

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(sprites):
            self.animation_frame = 0
            self.animating = False
            return

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def start_animating(self, pos):
        self.pos = pos
        self.animating = True


magic = {
    'agi': lambda: Magic('agi', 'Маленький огненный урон', 15, 'fire', 5, 6),
    'explosion': lambda: Magic('explosion', 'Взрыв', 40, 'fire', 20, 10)
}
