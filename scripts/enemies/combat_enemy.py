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
        self.text_animation_time = 7
        self.cur_text_animation_time = 0

        self.text_animation_state = 'idle'
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
        miss = {
            "miss": 1,
            'no': 0
        }
        if 'miss' in self.stats:
            s = miss[choices(["miss", "no"], weights=[self.stats["miss"], 1 - self.stats["miss"]])[0]]
        else:
            s = miss[choices(["miss", "no"], weights=[0, 1])[0]]
        if s == 0:
            # critical
            if damage_type == 'physical':
                crit = {
                    'crit': 1,
                    'no': 0
                }
                s = crit[choices(["crit", "no"], weights=[0.1, 0.9])[0]]
                damage *= max(2.5 * s, 1)
                self.text_animation_state = 'crit' if s else 'damage'
            # weak
            elif any(damage_type == weakness for weakness in self.stats['weaknesses']):
                damage *= 1.5
                self.text_animation_state = 'weak'
            # resist
            elif any(damage_type == resist for resist in self.stats['type']):
                damage *= .6
                self.text_animation_state = 'resist'
            else:
                self.text_animation_state = 'damage'

            self.hp -= damage
            self.received_damage = damage

            if self.hp <= 0:
                self.dead = True
            if once:
                return self.animate_once('hurt')
            self.set_animation('hurt')
        else:
            self.received_damage = 'MISS'
            self.text_animation_state = "damage"
            return self.animate_once('idle')

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

    def draw_special_effect(self, surface, font):
        if self.text_animation_state == 'idle':
            return
        self.draw_received_damage(surface, font)
        if self.text_animation_state != 'damage':

            state_to_image = {'crit': CombatEnemy.crit_image,
                              'weak': CombatEnemy.weak_image,
                              'resist': CombatEnemy.resist_image}
            image = state_to_image[self.text_animation_state]
            image.set_alpha((self.text_animation_time - self.cur_text_animation_time) / self.text_animation_time * 255)
            rect = image.get_rect()
            rect.topleft = self.position[0] - rect[2] // 2, self.position[1] + rect[3]
            surface.blit(image, rect)
        self.cur_text_animation_time += .1
        if self.cur_text_animation_time >= self.text_animation_time:
            self.cur_text_animation_time = 0
            self.text_animation_state = 'idle'

    def draw_received_damage(self, surface, font):
        if self.text_animation_state == 'idle':
            return
        if self.received_damage != "MISS":
            text_surface = font.render(f'{round(self.received_damage, 2)}', True, (255, 128, 0))
        else:
            text_surface = font.render(f'{self.received_damage}', True, (255, 128, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.position[0] + text_rect[2] // 2, self.position[1]
        surface.blit(text_surface, text_rect)

    def level_up(self):
        self.stats["endurance"] += 1
        self.stats["xp"] *= 1.05
