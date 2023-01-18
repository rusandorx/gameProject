import os
from abc import abstractmethod, ABCMeta
from random import choices, randint

import pygame
import zope.interface

from EffectsParticle import EffectsParticle
from combat_effects import IEffectAppliable, Effect
from spritesheet import SpriteSheet


@zope.interface.implementer(IEffectAppliable)
class CombatEnemy(pygame.sprite.Sprite, metaclass=ABCMeta):
    '''
    stats: {
        "strength": int,
        "endurance": int,
        "type": [Types],
        "weaknesses" [Types],
        "actions": {
            attack: .4,
            magic: .2,
            ...
        }
    }
    '''

    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(*groups)
        self.effects = {}
        self.active = True
        self.player = player
        self.name = name
        self.max_hp = hp * (lvl * .05)
        self.hp = self.max_hp
        self.lvl = lvl
        self.stats = stats
        self.position = position
        self.boss = False

        self.sprites = []
        self.actions_to_methods = {
            'attack': self.attack,
            'magic': self.magic
        }
        self.actions = self.stats['actions']
        self.sprite_state = 'idle'
        self.animation_frame = 0
        self.animation_speed = .1
        self.return_to_idle = False
        self.stop_at_last_frame = False
        self.dead = False
        self.outstroked = False
        self.on_animation_end = []
        self.on_turn_end = []
        self.load_assets()
        self.particle = EffectsParticle(self)

    def animation_length(self, animation):
        return len(self.sprites[animation])

    def animate_once(self, sprite_state):
        if self.dead:
            return
        self.sprite_state = sprite_state
        self.animation_frame = 0
        self.return_to_idle = True

    def animate_to_last_frame(self, animate_state):
        self.sprite_state = animate_state
        self.animation_frame = 0
        self.return_to_idle = False
        self.stop_at_last_frame = True

    @abstractmethod
    def load_assets(self):
        pass

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        if self.stop_at_last_frame and int(self.animation_frame) >= len(sprites) - 1:
            self.animate_ended()
            return

        self.animation_frame += self.animation_speed * 0.5
        if self.animation_frame >= len(sprites):
            self.animation_frame = 0
            if self.return_to_idle:
                self.return_to_idle = False
                self.sprite_state = 'idle'
                self.animate_ended()
                return

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def attack(self):
        self.animate_once('attack')
        self.player.take_damage(self.stats['attack'], 'physical')

    def magic(self):
        # TODO: Magic
        self.attack()

    def take_damage(self, damage, damage_type, once=True):
        if damage_type == 'physical':
            take_damage = damage * 0.95 ** self.stats['endurance']
            crete = {
                'crete': 1,
                'no': 0
            }
            s = crete[choices(["crete", "no"], weights=[0.2, 0.8])[0]]
            take_damage *= max(
                4.5 * s, 1)
            self.hp -= take_damage
        else:
            self.hp -= damage * (1.5 if any(stat == damage_type for stat in self.stats['type']) else 1)
        if self.hp <= 0:
            self.dead = True
        if once:
            return self.animate_once('hurt')
        self.set_animation('hurt')

    def set_animation(self, animation):
        if self.dead:
            return
        self.sprite_state = animation
        self.animation_frame = 0
        self.return_to_idle = False
        self.stop_at_last_frame = False

    def die(self):
        self.animate_to_last_frame('die')
        self.on_animation_end.append(self.set_active)

    def set_active(self, value=False):
        self.active = value

    def update(self):
        self.animate()

    def random_action(self):
        self.actions_to_methods[
            choices([*self.actions.keys()], weights=[action for action in self.actions.values()])[0]]()

    def animate_ended(self):
        for cb in self.on_animation_end:
            cb()
        self.on_animation_end.clear()

    def return_object_to_apply(self):
        return self

    def handle_effects_per_turn(self):
        to_delete = []
        for effect, count in self.effects.items():
            self.effects[effect] = count - 1
            if self.effects[effect] <= 0:
                effect.on_exit(self)
                to_delete.append(effect)
                continue

            effect.each_turn(self)
        for item in to_delete:
            del self.effects[item]

    def add_effect(self, effect: Effect):
        effect.on_apply(self)
        same_effects = tuple(filter(lambda eff: eff.name == effect.name, self.effects.keys()))
        if len(same_effects) > 0:
            for eff in same_effects:
                del self.effects[eff]
        self.effects[effect] = effect.turn_count

    def draw_particle_effects(self, surface, after_bg=True):
        for effect in self.effects:
            if after_bg:
                self.particle.draw_after(surface, effect.particle_color)
            else:
                self.particle.draw_before(surface, effect.particle_color)


class SkeletonEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        for i in range(lvl - 1):
            self.level_up()

    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/skeleton/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack_3.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 3, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 2, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 5, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


class NecromancerEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.animation_speed = 0.3
        self.stats["attack"] *= lvl
        self.boss = True
        for i in range(lvl - 1):
            self.level_up()

    def load_assets(self):
        graphics_path = '../graphics/ui/combat/sprites/necromancer/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind_Idle.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 7, (0, 0, 0)) +
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Taunt.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 17, (0, 0, 0)) +
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Idle1.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 7, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Attack.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 13, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 5, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (640, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Necromancer_creativekind-Dead.png')).load_strip(
                        pygame.Rect(0, 0, 160, 128), 9, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


class KnightEnemy(CombatEnemy):
    def __init__(self, name, lvl, hp, stats, position, player, *groups):
        super().__init__(name, lvl, hp, stats, position, player, *groups)
        self.stats["attack"] *= lvl
        for i in range(lvl - 1):
            self.level_up()

    def load_assets(self):
        if self.lvl <= 10:
            graphics_path = '../graphics/ui/combat/sprites/Knight_1/'
        elif self.lvl <= 15:
            graphics_path = '../graphics/ui/combat/sprites/Knight_2/'
        else:
            graphics_path = '../graphics/ui/combat/sprites/Knight_3/'
        self.sprites = {
            'idle': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Idle.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
            'attack': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Attack 3.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 4, (0, 0, 0)))),
            'hurt': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Hurt.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 2, (0, 0, 0)))),
            'die': list(
                map(lambda sprite: pygame.transform.flip(pygame.transform.scale(sprite, (512, 512)), True, False),
                    SpriteSheet(os.path.join(graphics_path, 'Dead.png')).load_strip(
                        pygame.Rect(0, 0, 128, 128), 6, (0, 0, 0))))
        }
        self.image = self.sprites[self.sprite_state][self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def level_up(self):
        self.stats["endurance"] *= 1.05
        self.stats["xp"] *= 1.05


enemies = {
    'skeleton': lambda position, player: SkeletonEnemy('skeleton', randint(1, 5), 30, {
        'attack': 0.8,
        'endurance': 10,
        'weaknesses': ['light'],
        'type': ['dark'],
        'xp': 5,
        'actions': {
            'attack': .7,
            'magic': .3,
        },
    }, position, player),
    'necromancer': lambda position, player: NecromancerEnemy('necromancer', randint(20, 30), 100, {
        'attack': 2,
        'endurance': 50,
        'weaknesses': [],
        'type': ['light'],
        'xp': 50,
        'actions': {
            'attack': .95,
            'magic': .05,
        },
    }, position, player),
    'knight': lambda position, player: KnightEnemy('knight', randint(5, 20), 30, {
        'attack': 2,
        'endurance': 10,
        'weaknesses': [],
        'type': ['light'],
        'xp': 7,
        'actions': {
            'attack': .7,
            'magic': .3,
        },
    }, position, player)
}
