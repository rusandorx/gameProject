import math
from random import randint

import pygame

from player.combat_player import CombatPlayer
from states.state import State
from math import pi
from sounds import Sound

from enemies import enemies


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
        self.enemies = [enemies[enemy_name]((self.game.width * 5 / 6 - _ * 256, 400 + 15 * math.cos(_))) for _ in range(self.enemies_count)]
        self.main_group.add(self.enemies)

        self.menu_image = pygame.transform.scale(pygame.image.load('../graphics/ui/combat/combat_menu.png'), (256, 256))
        self.enemy_index = 0
        self.state = 'idle'

    def update(self, key_state):
        if key_state['confirm']:
            self.enemies[0].take_damage(*self.player_sprite.attack())
            if self.enemies_count == 1:
                pass
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
