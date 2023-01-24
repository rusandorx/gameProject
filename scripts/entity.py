from abc import ABCMeta, abstractmethod

import pygame
import zope

from combat_effects import Effect, IEffectAppliable


@zope.interface.implementer(IEffectAppliable)
class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.stop_at_last_frame = False
        self.return_to_idle = False
        self.sprite_state = 'idle'
        self.animation_frame = 0
        self.particle = None
        self.effects, self.stats = {}, {}

    @abstractmethod
    def load_assets(self):
        pass

    def animation_ended(self):
        for cb in self.on_animation_end:
            cb()
        self.on_animation_end.clear()

    def return_object_to_apply(self):
        return self

    def handle_effects_per_turn(self):
        to_delete = []
        for effect, count in self.effects.items():
            self.effects[effect] = count - 1
            effect.each_turn(self)
            if self.effects[effect] <= 0:
                effect.on_exit(self)
                to_delete.append(effect)

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
        if not len(self.effects.keys()):
            return

        self.particle.set_colors(list(map(lambda eff: eff.particle_color, self.effects)))
        if after_bg:
            self.particle.draw_after(surface)
        else:
            self.particle.draw_before(surface)

    def attack(self, target):
        self.animate_once('attack')
        target.take_damage(self.stats['attack'], 'physical')

    def animate_once(self, animation):
        self.animation_frame = 0
        self.sprite_state = animation
        self.return_to_idle = True

    def animate_to_last_frame(self, animation):
        self.sprite_state = animation
        self.animation_frame = 0
        self.return_to_idle = False
        self.stop_at_last_frame = True

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        if self.stop_at_last_frame and int(self.animation_frame) >= len(sprites) - 1:
            self.animation_ended()
            return

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(sprites):
            self.animation_frame = 0
            if self.return_to_idle:
                self.return_to_idle = False
                self.sprite_state = 'idle'
                self.animation_ended()
                return

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.rect.center)