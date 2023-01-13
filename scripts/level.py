# import pygame
# from pytmx.util_pygame import load_pygame
#
# from obstacle import Obstacle
# from player import Player
# from scripts.settings import TILESIZE
# from enemy import Enemy
#
#
# class Level:
#     def __init__(self):
#         self.display_surface = pygame.display.get_surface()
#
#         # спрайты переднего фона сортируются по Y для придания эффекта глубины
#         self.main_group = YSortCameraGroup()
#         # задний план рендерится без сортировки
#         self.background_sprites = pygame.sprite.Group()
#         self.shadow_sprites = pygame.sprite.Group()
#         # со спрайтами препятствий происходят коллизии
#         self.obstacle_sprites = pygame.sprite.Group()
#
#         self.create_map()
#
#     def create_map(self):
#         map_data = load_pygame('../map/game_map/map.tmx')
#
#         for x, y, image in map_data.get_layer_by_name('background'):
#             if image != 0:
#                 Obstacle((x * TILESIZE, y * TILESIZE), [self.background_sprites], map_data.images[image])
#
#         for x, y, image in map_data.get_layer_by_name('shadows'):
#             if image != 0:
#                 Obstacle((x * TILESIZE, y * TILESIZE), [self.background_sprites], map_data.images[image])
#
#         for x, y, image in map_data.get_layer_by_name('content'):
#             if image != 0:
#                 Obstacle((x * TILESIZE, y * TILESIZE), [self.main_group, self.obstacle_sprites], map_data.images[image])
#
#         map_player = map_data.get_object_by_name('player')
#         self.player = Player((map_player.x, map_player.y), [self.main_group], self.obstacle_sprites)
#
#
#         for entity in map_data.get_layer_by_name('entities'):
#             if entity.name != "player":
#                 Enemy((entity.x, entity.y), [self.main_group], self.player, entity.name)
#
#     def run(self):
#         self.main_group.custorm_draw(self.player, [self.background_sprites, self.shadow_sprites])
#         self.main_group.update()
#
#
# class YSortCameraGroup(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.half_width = self.display_surface.get_width() // 2
#         self.half_height = self.display_surface.get_height() // 2
#         self.offset = pygame.math.Vector2()
#
#     def custorm_draw(self, player: Player, additional_groups: [pygame.sprite.AbstractGroup]):
#         self.offset.x = player.rect.centerx - self.half_width
#         self.offset.y = player.rect.centery - self.half_height
#
#
#
#         for group in additional_groups:
#             for sprite in group.sprites():
#                 self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)
#
#         for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
#             offset_position = sprite.rect.topleft - self.offset
#             self.display_surface.blit(sprite.image, offset_position)
#
