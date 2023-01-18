from abc import ABC

import zope
from zope.interface import Interface


class IEffectAppliable(Interface):
    effects = zope.interface.Attribute('Effects in combat')
    stats = zope.interface.Attribute('Entity stats')

    def return_object_to_apply():
        ''' Returns an object to which the effects will be applied. '''


class Effect(ABC):
    def __init__(self, options: dict):
        self.options = options
        self.name = options.get('name', 'Эффект')
        self.turn_count = options.get('turn_count', 1)
        self.particle_color = options.get('color', (255, 255, 255))

    def on_apply(self, entity: IEffectAppliable):
        pass

    def on_exit(self, entity: IEffectAppliable):
        pass

    def each_turn(self, entity: IEffectAppliable):
        pass


class BurnEffect(Effect):
    def __init__(self, options):
        super().__init__(options)
        self.damage = options['damage']

    def each_turn(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.hp = max(entity_obj.hp - self.damage, 0)

