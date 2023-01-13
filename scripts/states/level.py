import pygame
from pytmx.util_pygame import load_pygame

from obstacle import Obstacle
from player import Player
from scripts.settings import TILESIZE
from states.state import State
from enemy import Enemy


class Level(State):
    def __init__(self, game):
        super().__init__(game)
        self.display_surface = self.game.display

        # спрайты переднего фона сортируются по Y для придания эффекта глубины
        self.main_group = YSortCameraGroup()
        # задний план рендерится без сортировки
        self.background_sprites = pygame.sprite.Group()
        self.shadow_sprites = pygame.sprite.Group()
        # со спрайтами препятствий происходят коллизии
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        map_data = load_pygame('../map/game_map/map.tmx')

        for x, y, image in map_data.get_layer_by_name('background'):
            if image != 0:
                Obstacle((x * TILESIZE, y * TILESIZE), [self.background_sprites], map_data.images[image])

        for x, y, image in map_data.get_layer_by_name('shadows'):
            if image != 0:
                Obstacle((x * TILESIZE, y * TILESIZE), [self.background_sprites], map_data.images[image])

        for x, y, image in map_data.get_layer_by_name('content'):
            if image != 0:
                Obstacle((x * TILESIZE, y * TILESIZE), [self.main_group, self.obstacle_sprites], map_data.images[image])

        map_player = map_data.get_object_by_name('player')
        self.player = Player((map_player.x, map_player.y), [self.main_group], self.obstacle_sprites)


        for entity in map_data.get_layer_by_name('entities'):
            if entity.name != "player":
                Enemy((entity.x, entity.y), [self.main_group], self.player, entity.name)

    def update(self, key_state):
        self.main_group.update()

    def render(self, display):
        self.main_group.custom_draw(display, self.player, [self.background_sprites, self.shadow_sprites])


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def custom_draw(self, display, player: Player, additional_groups: [pygame.sprite.AbstractGroup]):
        half_width = display.get_width() // 2
        half_height = display.get_height() // 2
        offset = pygame.math.Vector2()
        offset.x = player.rect.centerx - half_width
        offset.y = player.rect.centery - half_height

        for group in additional_groups:
            for sprite in group.sprites():
                display.blit(sprite.image, sprite.rect.topleft - offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - offset
            display.blit(sprite.image, offset_position)


