import pygame
from pytmx.util_pygame import load_pygame

from obstacle import Obstacle
from player import Player


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # спрайты переднего фона сортируются по Y для придания эффекта глубины
        self.foreground_sprites = YSortCameraGroup()
        # задний план рендерится без сортировки
        self.background_sprites = pygame.sprite.Group()
        # со спрайтами препятствий происходят коллизии
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        map_data = load_pygame('../map/game_map/map.tmx')

        for x, y, image in map_data.get_layer_by_name('background'):
            if image != 0:
                Obstacle((x * 64, y * 64), [self.background_sprites], map_data.images[image])

        for x, y, image in map_data.get_layer_by_name('content'):
            if image != 0:
                Obstacle((x * 64, y * 64), [self.foreground_sprites, self.obstacle_sprites], map_data.images[image])

        map_player = map_data.get_object_by_name('player')
        self.player = Player((map_player.x, map_player.y), [self.foreground_sprites], self.obstacle_sprites)

    def run(self):
        self.background_sprites.draw(self.display_surface)
        self.foreground_sprites.custorm_draw(self.player)
        self.foreground_sprites.update()


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
            self.display_surface.blit(sprite.image, offset_position)
