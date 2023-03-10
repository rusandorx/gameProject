from random import choice

import pygame
from pytmx.util_pygame import load_pygame

from enemies.enemies_list import get_enemy_pattern
from enemy import Enemy, ENEMIES_BACKGROUNDS
from obstacle import Obstacle
from player.level_player import LevelPlayer
from scripts.settings import TILESIZE
from states.combat import Combat
from states.pause_menu import PauseMenu
from states.state import State


class Level(State):
    def __init__(self, game):
        super().__init__(game)
        self.display_surface = self.game.display

        # спрайты переднего фона сортируются по Y для придания эффекта глубины
        self.main_group = YSortCameraGroup()
        # задний план рендерится без сортировки
        self.background_sprites = pygame.sprite.Group()
        # со спрайтами препятствий происходят коллизии
        self.obstacle_sprites = pygame.sprite.Group()
        self.up_group = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        map_data = load_pygame('../map/game_map/map.tmx')

        for layer_name in map_data.layernames:
            if layer_name in ('content', 'entities'):
                continue
            for x, y, image in map_data.get_layer_by_name(layer_name):
                if image != 0:
                    Obstacle((x * TILESIZE, y * TILESIZE),
                             (self.background_sprites if not layer_name.startswith('top') else self.up_group,),
                             map_data.images[image])

        for x, y, image in map_data.get_layer_by_name('content'):
            if image != 0:
                Obstacle((x * TILESIZE, y * TILESIZE), (self.main_group, self.obstacle_sprites), map_data.images[image])

        map_player = map_data.get_object_by_name('player')
        self.player = LevelPlayer((map_player.x, map_player.y), (self.main_group,), self.obstacle_sprites)

        for entity in map_data.get_layer_by_name('entities'):
            if entity.name != "player":
                Enemy((entity.x, entity.y), (self.main_group, ), self.player, entity.name, self.attack_callback)

    def attack_callback(self, enemy_name, level_name):
        background = ENEMIES_BACKGROUNDS.get(enemy_name, choice(('Battleground1', 'Battleground4')))
        combat = Combat(self.game, get_enemy_pattern(enemy_name, self.game.player.lvl), level_name, background)
        combat.enter_state()

    def update(self, key_state):
        if key_state['start']:
            pause_menu = PauseMenu(self.game)
            pause_menu.enter_state()
        self.main_group.update()
        self.player.update(key_state)

    def render(self, display):
        half_width = display.get_width() // 2
        half_height = display.get_height() // 2
        offset = pygame.math.Vector2()
        offset.x = self.player.rect.centerx - half_width
        offset.y = self.player.rect.centery - half_height
        offset_position = self.player.rect.topleft - offset
        self.main_group.custom_draw(display, self.player, [self.background_sprites], [self.up_group])
        pygame.draw.rect(display, "gray",
                         (offset_position.x, offset_position.y,
                          32,
                          5))
        pygame.draw.rect(display, (int(255 * (1 - self.game.player.hp / self.game.player.max_hp)),
                                   int(255 * self.game.player.hp / self.game.player.max_hp), 0),
                         (offset_position.x, offset_position.y,
                          (self.game.player.hp / self.game.player.max_hp) * 32,
                          5))


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def custom_draw(self, display, player, bottom_groups: [pygame.sprite.AbstractGroup],
                    up_groups: [pygame.sprite.AbstractGroup]):
        half_width = display.get_width() // 2
        half_height = display.get_height() // 2
        offset = pygame.math.Vector2()
        offset.x = player.rect.centerx - half_width
        offset.y = player.rect.centery - half_height

        for group in bottom_groups:
            for sprite in group.sprites():
                display.blit(sprite.image, sprite.rect.topleft - offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - offset
            display.blit(sprite.image, offset_position)

        for group in up_groups:
            for sprite in group.sprites():
                display.blit(sprite.image, sprite.rect.topleft - offset)
