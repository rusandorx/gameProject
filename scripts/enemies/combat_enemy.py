import os
from abc import ABCMeta
from random import choices

import pygame

from EffectsParticle import EffectsParticle
from entity import Entity


class CombatEnemy(Entity, metaclass=ABCMeta):
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
    crit_image = None
    weak_image = None
    resist_image = None

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
        self.text_animation_time = 10
        self.cur_text_animation_time = 0

        self.text_animation_state = 'none'
        self.load_assets()
        self.particle = EffectsParticle(self)

    def load_assets(self):
        path = '../graphics/ui/combat/'
        if CombatEnemy.weak_image is None:
            CombatEnemy.weak_image = pygame.image.load(os.path.join(path, 'weak.png'))
        if CombatEnemy.crit_image is None:
            CombatEnemy.crit_image = pygame.image.load(os.path.join(path, 'crit.png'))
        if CombatEnemy.resist_image is None:
            CombatEnemy.resist_image = pygame.image.load(os.path.join(path, 'resist.png'))

    def animate_once(self, sprite_state):
        if self.dead:
            return
        super().animate_once(sprite_state)

    def attack(self, target=None):
        if target is None:
            target = self.player
        super().attack(target)

    def magic(self):
        self.attack()

    def take_damage(self, damage, damage_type, once=True):
        damage = damage * .95 ** self.stats['endurance']

        # critical
        if damage_type == 'physical':
            crit = {
                'crit': 1,
                'no': 0
            }
            s = crit[choices(["crit", "no"], weights=[0.1, 0.9])[0]]
            damage *= max(2.5 * s, 1)
        # weak
        elif any(damage_type == weakness for weakness in self.stats['weaknesses']):
            damage *= 1.5
        # resist
        elif any(damage_type == resist for resist in self.stats['type']):
            damage *= .6

        self.hp -= damage

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

    @staticmethod
    def draw_special_effects(surface, effect):
        if effect == 'weak':
            surface.blit(CombatEnemy.weak_image)
        elif effect == 'crit':
            surface.blit(CombatEnemy.crit_image)
        elif effect == 'resist':
            surface.blit(CombatEnemy.resist_image)

    @staticmethod
    def draw_text_effects(surface, text):
        pass

    def animate_text(self):
        if self.text_animation_state == 'none':
            return
        self.cur_text_animation_time += .1
