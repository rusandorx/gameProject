import math
from math import pi
from random import randint

import pygame

from enemies import enemies, CombatEnemy
from player.combat_player import CombatPlayer
from states.state import State
from utils import get_outline
from sounds import Sound


class Combat(State):
    def __init__(self, game, enemy_name, level_name):
        super().__init__(game)
        Sound.stop_all()

        self.level_name = level_name
        self.main_group = pygame.sprite.Group()
        self.background = pygame.image.load('../graphics/Battleground1/Bright/Battleground1.png')
        self.background_rect = self.background.get_rect()
        self.combat_player = CombatPlayer((200, 400), self.game.player)
        self.main_group.add(self.combat_player)

        self.enemies_count = randint(1, 3)
        self.enemies: [CombatEnemy] = [
            enemies[enemy_name]((self.game.width * 5 / 6 - _ * 256, 400 + 25 * randint(-2, 2)), self.combat_player)
            for _ in
            range(self.enemies_count)]
        self.main_group.add(self.enemies)

        self.menu_image = pygame.transform.scale(pygame.image.load('../graphics/ui/combat/combat_menu.png'), (256, 256))
        self.enemy_index = self.enemies_count - 1
        self.enemies_turn = 0

        self.state = 'idle'
        self.action = 'idle'
        self.actions = {
            'attack': self.player_attack,
            'magic': self.player_magic,
        }
        self.outline = False

    def update(self, key_state):
        self.update_enemies()
        if self.state == 'enemies':
            if self.enemies_turn >= self.enemies_count:
                self.state = 'idle'
            else:
                if self.state != 'enemy action':
                    self.enemies[self.enemies_turn].random_action()
                    self.enemies[self.enemies_turn].on_animate_end.append(self.enemy_animation_ended)
                    self.state = 'enemy action'
        else:
            if self.state != 'player animation':
                self.handle_keys(key_state)
        self.game.reset_keys()
        self.main_group.update()

    def update_enemies(self):
        rest_enemies = list(filter(lambda x: x.active, self.enemies))
        rest_enemies_count = len(rest_enemies)
        print(self.state)
        if rest_enemies_count == 0:
            if self.state != 'enemies dead':
                self.enemies[0].on_animate_end.append(self.on_all_enemies_dead)
                self.state = 'enemies dead'
        elif rest_enemies_count != self.enemies_count:
            self.enemies = rest_enemies
            self.enemies_count = rest_enemies_count
            self.enemy_index = self.enemies_count - 1

    def render(self, surface):
        surface.blit(self.background, self.background_rect)
        for i in self.enemies:
            if i.active:
                self.game.draw_text(surface, f"{round(i.hp, 1)} / {round(i.max_hp, 1)}", (255,
                                                                                          255, 255),
                                    i.position[0] + 30, i.position[1] - 40)
                pygame.draw.rect(surface, "gray",
                                 (i.position[0] - 20, i.position[0] - 20,
                                  128,
                                  10))
                pygame.draw.rect(surface, (int(255 * (1 - i.hp / i.max_hp)),
                                           int(255 * (i.hp / i.max_hp)), 0),
                                 (i.position[0] - 20, i.position[1] - 20,
                                  (i.hp / i.max_hp) * 128,
                                  10))
        pygame.draw.arc(surface, (int(255 * (1 - self.game.player.hp / self.game.player.max_hp)),
                                  int(255 * self.game.player.hp / self.game.player.max_hp), 0),
                        (self.combat_player.rect.centerx - 160, self.combat_player.rect.centery + 200, 225, 100),
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
        self.combat_player.attack(self.enemies[self.enemy_index])
        self.state = 'player_animation'
        self.combat_player.on_animation_ended.append(self.player_animation_ended)

    def player_magic(self):
        pass

    def enemy_animation_ended(self):
        self.enemies_turn += 1
        if self.enemies_turn > self.enemies_count:
            self.state = 'idle'
        else:
            self.state = 'enemies'

    def player_animation_ended(self):
        self.enemies_turn = 0
        if self.state != 'enemies dead':
            self.state = 'enemies'

    def on_all_enemies_dead(self):
        self.exit_state()
        self.level_name.die()
        Sound.stop_all()
