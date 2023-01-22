from random import randint

from enemies.knight import KnightEnemy
from enemies.necromancer import NecromancerEnemy
from enemies.skeleton import SkeletonEnemy, SkeletonSpearman, SkeletonWarrior
from enemies.zombie import ZombieEnemy

ENEMIES = {
    'skeleton': lambda position, player: SkeletonEnemy('skeleton', randint(1, 5), 30, {
        'attack': 0.8,
        'endurance': 10,
        'weaknesses': ['light'],
        'type': ['dark'],
        'xp': 5,
        'actions': {
            'attack': .5,
            'strong_attack': .3,
            'bleeding_attack': .2
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
            'attack': .8,
            'buff': .1,
            'debuff_attack': .1
        },
    }, position, player),
    'zombie': lambda position, player: ZombieEnemy('zombie', randint(10, 15), 25, {
        'attack': 4,
        'endurance': 2,
        'weaknesses': ['fire'],
        'type': ['dark'],
        'xp': 15,
        'actions': {
            'attack': .7,
            'heal': .3
        },
    }, position, player),
    'SkeletonSpearman': lambda position, player: SkeletonSpearman('Spearman', randint(5, 15), 50, {
        'attack': 1.2,
        'endurance': 20,
        'miss': 0.2,
        'weaknesses': ['light'],
        'type': ['dark', 'physical'],
        'xp': 7,
        'actions': {
            'attack': .5,
            'strong_attack': .3,
            'bleeding_attack': .2
        },
    }, position, player),
    'SkeletonWarrior': lambda position, player: SkeletonWarrior('Warrior', randint(10, 20), 50, {
        'attack': 1.5,
        'manaburn': 2,
        'endurance': 30,
        'miss': 0.25,
        'weaknesses': ['light'],
        'type': ['dark', 'physical'],
        'xp': 10,
        'actions': {
            'attack': .5,
            'strong_attack': .3,
            'bleeding_attack': .2
        },
    }, position, player)
}
