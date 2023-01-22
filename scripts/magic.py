import os
import random

import pygame

from combat_effects import BurnEffect, DefenceBuff, ColorEffect
from enemies.combat_enemy import CombatEnemy
from player.combat_player import CombatPlayer
from spritesheet import SpriteSheet


class Magic(pygame.sprite.Sprite):
    def __init__(self, options: dict, *groups):
        super().__init__(*groups)
        self.name = options.get('name', 'magic')
        self.description = options.get('description', 'Описание')
        self.damage = options.get('damage', 5)
        self.damage_type = options.get('damage_type', 'physical')
        self.cost = options.get('cost', 5)
        self.sprites_count = options.get('sprites_count', 0)
        self.need_target = options.get('need_target', True)
        self.sprites_size = options.get('sprites_size', (256, 256))
        self.options = options
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
        player.animate_once(f'{self.damage_type}-magic')
        if target is not None:
            target.take_damage((player.player.lvl * .05) * self.damage, self.damage_type, False)
        self.on_animation_end.append(lambda: target.set_animation('idle'))
        player.player.mp -= self.cost

    def animation_ended(self):
        for cb in self.on_animation_end:
            cb()

    def can_be_used(self, player):
        return player.mp >= self.cost


class HealMagic(Magic):
    def __init__(self, options, *groups):
        super().__init__(options, *groups)
        self.heal_hp = options.get('heal_hp', 10)

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = [pygame.image.load(os.path.join(path, 'sprites.png'))]
        self.image = self.sprites[0]
        self.rect = pygame.Rect(0, 0, 0, 0)

    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.add_effect(ColorEffect({'name': 'color', 'turn_count': 1, 'color': (32, 250, 30)}))
        player.animate_once(f'{self.damage_type}-magic')
        player.on_animation_end.append(self.animation_ended)
        player.player.hp += self.heal_hp
        player.player.hp = player.player.max_hp if player.player.hp > player.player.max_hp else player.player.hp
        player.player.mp -= self.cost

    def animate(self):
        pass

    def can_be_used(self, player):
        if not super().can_be_used(player):
            return False
        return player.hp < player.max_hp


class DarkMagic(Magic):
    def __init__(self, options: dict, *groups):
        super().__init__(options, *groups)
        self.self_damage = self.options.get('self_damage', 0)

    def use(self, player: CombatPlayer, target: CombatEnemy):
        super().use(player, target)
        player.player.hp -= self.self_damage

    def can_be_used(self, player):
        if not super().can_be_used(player):
            return False
        return player.hp - self.self_damage > 0


class LightMagic(Magic):
    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.animate_once(f'{self.damage_type}-magic')
        if target.boss:
            is_instakill = False
        else:
            is_instakill = \
                random.choices([True, False], weights=[self.options['instakill'], 1 - self.options['instakill']])[0]
        target.take_damage((player.player.lvl * .05) * self.damage if not is_instakill else target.hp * 20,
                           self.damage_type,
                           False)
        self.on_animation_end.append(lambda: target.set_animation('idle'))
        player.player.mp -= self.cost


class FireMagic(Magic):
    def __init__(self, options: dict, *groups):
        super().__init__(options, *groups)
        self.burn_chance = options.get('burn_chance', 0)

    def use(self, player: CombatPlayer, target: CombatEnemy):
        burnt = random.choices((True, False), weights=(self.burn_chance, 1 - self.burn_chance))[0]
        if burnt:
            target.add_effect(BurnEffect({'name': 'burn', 'turn_count': 3, 'color': (192, 64, 0), 'damage': 1}))
        super().use(player, target)


class BuffMagic(Magic):
    def __init__(self, options: dict, *groups):
        super().__init__(options, *groups)
        self.effect = options.get('effect')

    def use(self, player: CombatPlayer, target: CombatEnemy):
        player.add_effect(self.effect)

    def load_assets(self):
        path = f'../graphics/ui/combat/magic/{self.name}/'
        self.icon = pygame.transform.scale(pygame.image.load(os.path.join(path, 'Icon.png')), (64, 64))
        self.sprites = [pygame.image.load(os.path.join(path, 'sprites.png'))]
        self.image = self.sprites[0]
        self.rect = pygame.Rect(0, 0, 0, 0)


magic = {
    'agi': lambda: FireMagic(
        {
            'name': 'agi',
            'description': 'Маленький огненный урон',
            'damage': 20,
            'damage_type': 'fire',
            'cost': 5,
            'sprites_count': 6,
            'sprites_size': (128, 128),
            'burn_chance': .2
        }
    ),
    'explosion': lambda: FireMagic(
        {
            'name': 'explosion',
            'description': 'Средний урон огнём',
            'damage': 50,
            'damage_type': 'fire',
            'cost': 20,
            'sprites_count': 14,
            'sprites_size': (64, 64),
            'burn_chance': .25
        }
    ),
    'dark-bolt': lambda: DarkMagic(
        {
            'name': 'dark-bolt',
            'description': 'Темная молния (-10 HP)',
            'damage': 30,
            'damage_type': 'dark',
            'cost': 10,
            'sprites_count': 10,
            'sprites_size': (77, 88),
            'self_damage': 10
        }
    ),
    'lightning': lambda: LightMagic(
        {
            'name': 'lightning',
            'description': 'Священная молния (шанс мгновенно убить обычного врага: 5%)',
            'damage': 25,
            'damage_type': 'light',
            'cost': 30,
            'sprites_count': 11,
            'sprites_size': (64, 128),
            'instakill': .05
        }
    ),
    'heal': lambda: HealMagic(
        {
            'name': 'heal',
            'description': 'Маленькое лечение',
            'damage_type': 'heal',
            'cost': 25,
            'sprites_count': 0,
            'heal_hp': 25,
            'need_target': False
        }
    ),
    'shield': lambda: BuffMagic(
        {
            'name': 'shield',
            'description': 'Понижает получаемый урон на 3 хода',
            'damage_type': 'buff',
            'cost': 15,
            'sprites_count': 0,
            'need_target': False,
            'effect': DefenceBuff({'name': 'def_up', 'turn_count': 3, 'color': (0, 64, 192), 'def_up_value': 1.3})
        }
    )
}
