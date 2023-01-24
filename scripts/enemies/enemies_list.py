from random import randint, choice

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
        'endurance': 20,
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
        'endurance': 10,
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
        'endurance': 10,
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


def get_enemy_pattern(level_enemy_name, player_lvl):
    if level_enemy_name == 'skeleton':
        if player_lvl < 2:
            return ['skeleton']
        if player_lvl < 4:
            return choice((['skeleton'], ['skeleton'] * 2))
        if player_lvl < 6:
            return choice((['skeleton'] * 2, ['skeleton'] * 3, ['SkeletonSpearman']))
        if player_lvl < 9:
            return choice((['skeleton'] * 3, ['SkeletonSpearman'], ['skeleton', 'SkeletonSpearman']))
        if player_lvl < 11:
            return choice((['SkeletonSpearman', 'skeleton'], ['SkeletonWarrior']))
        if player_lvl < 13:
            return choice((['SkeletonSpearman', 'skeleton', 'skeleton'], ['SkeletonWarrior', 'skeleton']))
        return choice(
            (['SkeletonSpearman', 'SkeletonSpearman', 'SkeletonWarrior'], ['SkeletonWarrior', 'skeleton', 'SkeletonSpearman']))
    if level_enemy_name == 'zombie':
        return choice((['zombie'], ['zombie'] * 2))
    if level_enemy_name == 'knight':
        return choice((['knight'] * 2, ['knight'] * 3, ['knight'] * 4))
    return [level_enemy_name]
