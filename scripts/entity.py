from abc import ABCMeta, abstractmethod

import pygame

from combat_effects import Effect


class Entity(pygame.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, *groups):
        super().__init__(*groups)

    @abstractmethod
    def load_assets(self):
        pass

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
