import os

import pygame

from spritesheet import SpriteSheet


class Magic:
    def __init__(self, name, description, damage, damage_type, cost, sprites_count):
        self.name = name
        self.description = description
        self.damage = damage
        self.damage_type = damage_type
        self.cost = cost
        self.sprites_count = sprites_count
        self.load_assets()

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = list(
            map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (128, 128)), True, False),
                SpriteSheet(os.path.join(path, f'sprites.png')).load_strip(
                    pygame.Rect(0, 0, 128, 128), self.sprites_count, (0, 0, 0))))


magic = {
    'agi': lambda: Magic('agi', 'Маленький огненный урон', 15, 'fire', 5, 6),
    'explosion': lambda: Magic('explosion', 'Взрыв', 40, 'fire', 20, 10)
}
