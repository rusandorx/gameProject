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


class DefenceBuff(Effect):
    def __init__(self, options):
        super().__init__(options)
        self.def_up_value = options['def_up_value']

    def on_apply(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.stats['endurance'] *= self.def_up_value

    def on_exit(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.stats['endurance'] = round(entity_obj.stats['endurance'] / self.def_up_value)


class BleedingEffect(Effect):
    def __init__(self, options):
        super().__init__(options)
        self.bleeding_value = options['bleeding_value']

    def each_turn(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.hp -= entity_obj.max_hp * self.bleeding_value


class AttackBuff(Effect):
    def __init__(self, options):
        super().__init__(options)
        self.attack_value = options['attack_value']
    def on_apply(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.stats['attack'] *= self.attack_value

    def on_exit(self, entity: IEffectAppliable):
        entity_obj = entity.return_object_to_apply()
        entity_obj.stats['attack'] = round(entity_obj.stats['attack'] / self.attack_value)


class ColorEffect(Effect):
    def __init__(self, options: dict):
        super().__init__(options)
        self.turn_count = 2
