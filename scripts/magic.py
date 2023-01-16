import os

import pygame

from enemies import CombatEnemy
from player.combat_player import CombatPlayer
from spritesheet import SpriteSheet


class Magic(pygame.sprite.Sprite):
    def __init__(self, name, description, damage, damage_type, cost, sprites_count, sprite_size=(256, 256),
                 need_target=True,
                 *groups):
        super().__init__(*groups)
        self.name = name
        self.description = description
        self.damage = damage
        self.damage_type = damage_type
        self.cost = cost
        self.sprites_count = sprites_count
        self.need_target = need_target
        self.sprites_size = sprite_size
        self.load_assets()
        self.animating = False
        self.animation_speed = .2
        self.animation_frame = 0
        self.pos = (0, 0)
        self.on_animation_end = []

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = list(
            map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (256, 256)), True, False),
                SpriteSheet(os.path.join(path, f'sprites.png')).load_strip(
                    pygame.Rect(0, 0, *self.sprites_size), self.sprites_count, (0, 0, 0))))
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
            self.animation_ended()
            return

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def start_animating(self, pos):
        self.pos = pos
        self.animating = True

    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.set_sprite_state_once(f'{self.damage_type}-magic')
        target.take_damage((player.player.lvl * .05) * self.damage, self.damage_type, False)
        self.on_animation_end.append(lambda: target.set_animation('idle'))
        player.player.mp -= self.cost

    def animation_ended(self):
        for cb in self.on_animation_end:
            cb()


class HealMagic(Magic):
    def __init__(self, name, description, heal_hp, damage_type, cost, sprites_count, *groups):
        super().__init__(name, description, heal_hp, damage_type, cost, sprites_count, (0, 0), False, *groups)
        self.heal_hp = heal_hp

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = [pygame.image.load(os.path.join(path, 'sprites.png'))]
        self.image = self.sprites[0]
        self.rect = pygame.Rect(0, 0, 0, 0)

    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.set_sprite_state_once(f'{self.damage_type}-magic')
        player.on_animation_end.append(self.animation_ended)
        player.player.hp += self.heal_hp
        player.player.hp = player.player.max_hp if player.player.hp > player.player.max_hp else player.player.hp
        player.player.mp -= self.cost

    def animate(self):
        pass


magic = {
    'agi': lambda: Magic('agi', 'Маленький огненный урон', 20, 'fire', 5, 6, (128, 128)),
    'explosion': lambda: Magic('explosion', 'Средний урон огнём', 50, 'fire', 20, 14, (64, 64)),
    'dark-bolt': lambda: Magic('dark-bolt', 'Темная молния', 30, 'dark', 10, 10, (77, 88)),
    'lightning': lambda: Magic('lightning', 'Священная молния', 25, 'light', 50, 11, (64, 128)),
    'heal': lambda: HealMagic('heal', 'Маленькое лечение', 20, 'buff', 25, 0)
}
