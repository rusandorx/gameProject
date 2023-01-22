from random import randint

from enemies.knight import KnightEnemy
from enemies.necromancer import NecromancerEnemy
from enemies.skeleton import SkeletonEnemy

ENEMIES = {
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
        'weaknesses': ['dark'],
        'type': ['light'],
        'xp': 7,
        'actions': {
            'attack': .7,
            'magic': .3,
        },
    }, position, player)
}
