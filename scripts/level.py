import pygame

from obstacle import Obstacle
from player import Player
from settings import *


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for i, row in enumerate(WORLD_MAP):
            for j, col in enumerate(row):
                x, y = i * TILESIZE, j * TILESIZE
                if col == 'x':
                    Obstacle((x, y),
                             [self.visible_sprites, self.obstacle_sprites], '../graphics/test/rock.png')
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)
                if col == 'g':
                    Obstacle((x, y), [self.visible_sprites], '../graphics/grass/grass_2.png')

    def run(self):
        self.visible_sprites.custorm_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custorm_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            if len(sprite.groups()) == 1:
                self.display_surface.blit(sprite.image, offset_position)
        self.display_surface.blit(player.image, player.rect.topleft - self.offset)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            if len(sprite.groups()) == 2:
                self.display_surface.blit(sprite.image, offset_position)
