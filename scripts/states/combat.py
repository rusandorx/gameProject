import math
from math import pi
from random import randint

import pygame

from enemies import enemies, CombatEnemy
from player.combat_player import CombatPlayer
from sounds import Sound
from states.state import State
from utils import get_outline


class Combat(State):
    def __init__(self, game, enemy_name):
        super().__init__(game)
        Sound.stop_all()

        self.main_group = pygame.sprite.Group()
        self.background = pygame.image.load('../graphics/Battleground1/Bright/Battleground1.png')
        self.background_rect = self.background.get_rect()
        self.player_sprite = CombatPlayer((200, 400), self.game.player)
        self.main_group.add(self.player_sprite)

        self.enemies_count = randint(1, 3)
        self.enemies: [CombatEnemy] = [enemies[enemy_name]((self.game.width * 5 / 6 - _ * 256, 400 + 15 * math.cos(_)))
                                       for _ in
                                       range(self.enemies_count)]
        self.main_group.add(self.enemies)

        self.menu_image = pygame.transform.scale(pygame.image.load('../graphics/ui/combat/combat_menu.png'), (256, 256))
        self.enemy_index = self.enemies_count - 1
        self.state = 'idle'
        self.action = 'idle'
        self.actions = {
            'attack': self.player_attack,
            'magic': self.player_magic,
        }
        self.outline = False

    def update(self, key_state):
        self.handle_keys(key_state)
        self.game.reset_keys()
        self.main_group.update()

    def render(self, surface):
        surface.blit(self.background, self.background_rect)
        pygame.draw.arc(surface, (int(255 * (1 - self.game.player.hp / self.game.player.max_hp)),
                                  int(255 * self.game.player.hp / self.game.player.max_hp), 0),
                        (self.player_sprite.rect.centerx - 160, self.player_sprite.rect.centery + 200, 225, 100),
                        pi,
                        (self.game.player.hp / self.game.player.max_hp) * 2 * pi + pi, 10)
        self.main_group.draw(surface)
        if self.outline:
            surface.blit(self.outline, (self.enemies[self.enemy_index].position[0] - 256,
                                        self.enemies[self.enemy_index].position[1] - 256))

    def handle_keys(self, key_state):
        if self.state == 'idle':
            if key_state['confirm']:
                if self.enemies_count == 1:
                    self.player_attack()
                else:
                    self.action = 'attack'
                    self.state = 'choose_enemy'

        elif self.state == 'choose_enemy':
            if key_state['left']:
                self.enemy_index = (self.enemy_index + 1) % self.enemies_count
            if key_state['right']:
                self.enemy_index = (self.enemy_index - 1) if self.enemy_index > 0 else self.enemies_count - 1
            if key_state['confirm']:
                self.actions[self.action]()
                self.state = 'idle'
                self.outline = False
                return
            self.outline = get_outline(self.enemies[self.enemy_index].image, (255, 255, 255))

    def player_attack(self):
        self.enemies[self.enemy_index].take_damage(*self.player_sprite.attack())

    def player_magic(self):
        pass
