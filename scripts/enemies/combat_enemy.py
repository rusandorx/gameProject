from abc import ABCMeta
from random import choices

import zope

from EffectsParticle import EffectsParticle
from combat_effects import IEffectAppliable
from entity import Entity


@zope.interface.implementer(IEffectAppliable)
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


