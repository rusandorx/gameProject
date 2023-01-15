from enum import Enum
from math import pi
from random import randint

import pygame

from enemies import enemies, CombatEnemy
from player.combat_player import CombatPlayer
from sounds import Sound
from spritesheet import SpriteSheet
from states.magic_menu import MagicMenu
from states.state import State
from utils import get_outline


class Combat(State):
    def __init__(self, game, enemy_name, level_name, count_enemy):
        super().__init__(game)
        Sound.stop_all()

        self.level_name = level_name
        self.main_group = pygame.sprite.Group()
        self.background = pygame.image.load('../graphics/Battleground1/Bright/Battleground1.png')
        self.background_rect = self.background.get_rect()
        self.combat_player = CombatPlayer((200, 400), self.game.player)
        self.main_group.add(self.combat_player)
        self.combat_menu = CombatMenu((0, 0))
        self.magic = None

        self.enemies_count = randint(*count_enemy)
        self.enemies: [CombatEnemy] = [
            enemies[enemy_name]((self.game.width * 5 / 6 - _ * 256, 400 + 25 * randint(-2, 2)), self.combat_player)
            for _ in
            range(self.enemies_count)]
        self.enemy_size = self.enemies[0].image.get_rect()[2:]
        print(self.enemy_size)
        self.main_group.add(self.enemies)

        self.enemy_index = self.enemies_count - 1
        self.enemies_turn = 0

        self.state = CombateState.IDLE
        self.action = CombateState.IDLE
        self.actions = {
            'attack': self.player_attack,
            'magic': self.player_magic,
        }
        self.outline = False

    def update(self, key_state):
        if self.magic and self.magic.animating:
            self.magic.update()
        self.update_enemies()
        if self.combat_player.player.hp <= 0:
            self.combat_player.on_animation_ended.append(self.game.load_states())
        if self.state == CombateState.ENEMIES:
            if self.enemies_turn >= self.enemies_count:
                self.state = CombateState.IDLE
            else:
                if self.state != CombateState.ENEMY_ANIMATION:
                    self.enemies[self.enemies_turn].random_action()
                    self.enemies[self.enemies_turn].on_animate_end.append(self.enemy_animation_ended)
                    self.state = CombateState.ENEMY_ANIMATION
        else:
            if self.state != CombateState.PLAYER_ANIMATION and self.state != CombateState.CHOOSE_MAGIC:
                self.handle_keys(key_state)
        self.game.reset_keys()
        self.main_group.update()
        self.combat_menu.update()

    def get_magic_index(self, index):
        if index == -1:
            self.state = CombateState.IDLE
            self.action = CombateState.IDLE
            return
        self.state = CombateState.CHOOSE_ENEMY
        self.action = 'magic'
        self.magic = self.game.player.magic[index]

    def update_enemies(self):
        rest_enemies = list(filter(lambda x: x.active, self.enemies))
        rest_enemies_count = len(rest_enemies)
        if rest_enemies_count == 0:
            if self.state != CombateState.ENEMIES_DEAD:
                self.enemies[0].on_animate_end.append(self.on_all_enemies_dead)
                self.state = CombateState.ENEMIES_DEAD
        elif rest_enemies_count != self.enemies_count:
            self.enemies = rest_enemies
            self.enemies_count = rest_enemies_count
            self.enemy_index = self.enemies_count - 1

    def render(self, surface):
        surface.blit(self.background, self.background_rect)
        for i in self.enemies:
            if i.active:
                self.game.draw_text(surface, f"{i.name} LVL {i.lvl}",
                                    ((min((max(1, i.lvl - self.game.player.lvl) * 64), 255)),
                                     (min((max(1, self.game.player.lvl - i.lvl) * 64), 255)),
                                     0),
                                    i.position[0] + 30, i.position[1] - 70)
                self.game.draw_text(surface,
                                    f"{round(i.hp, 1) if round(i.hp, 1) != 0.0 else '0.1'} / {round(i.max_hp, 1)}",
                                    (255,
                                     255,
                                     255),
                                    i.position[0] + 30, i.position[1] - 40)
                pygame.draw.rect(surface, "gray",
                                 (i.position[0] - 20, i.position[1] - 20,
                                  128,
                                  10))
                pygame.draw.rect(surface, (int(255 * (1 - i.hp / i.max_hp)),
                                           int(255 * (i.hp / i.max_hp)), 0),
                                 (i.position[0] - 20, i.position[1] - 20,
                                  (i.hp / i.max_hp) * 128,
                                  10))
        if self.game.player.hp > 0:
            pygame.draw.arc(surface, (int(255 * (1 - self.game.player.hp / self.game.player.max_hp)),
                                      int(255 * self.game.player.hp / self.game.player.max_hp), 0),
                            (self.combat_player.rect.centerx - 160, self.combat_player.rect.centery + 200, 225, 100),
                            pi,
                            (self.game.player.hp / self.game.player.max_hp) * 2 * pi + pi, 10)
        if self.state == CombateState.IDLE:
            surface.blit(self.combat_menu.image, (self.combat_player.position[0], self.combat_player.position[1] - 50))
        self.main_group.draw(surface)
        if self.outline and self.state == CombateState.CHOOSE_ENEMY:
            surface.blit(self.outline, (self.enemies[self.enemy_index].position[0] - self.enemy_size[0] * .5,
                                        self.enemies[self.enemy_index].position[1] - self.enemy_size[1] * .5))
        if self.magic and self.magic.animating:
            surface.blit(self.magic.image, self.magic.pos)

    def handle_keys(self, key_state):
        if self.state == CombateState.IDLE:
            if key_state['confirm']:
                self.action = 'attack'
                self.state = CombateState.CHOOSE_ENEMY
            elif key_state['l']:
                self.action = 'magic'
                self.state = CombateState.CHOOSE_MAGIC
                magicMenu = MagicMenu(self.game, self.get_magic_index)
                magicMenu.enter_state()


        elif self.state == CombateState.CHOOSE_ENEMY:
            if self.enemies_count == 1:
                self.actions[self.action]()
                self.outline = False
            elif key_state['left']:
                self.enemy_index = (self.enemy_index + 1) % self.enemies_count
            elif key_state['right']:
                self.enemy_index = (self.enemy_index - 1) if self.enemy_index > 0 else self.enemies_count - 1
            elif key_state['cancel']:
                self.state = CombateState.IDLE
            elif key_state['confirm']:
                self.actions[self.action]()
                self.outline = False
                return
            self.outline = get_outline(self.enemies[self.enemy_index].image, (255, 255, 255))

    def player_attack(self):
        self.combat_player.attack(self.enemies[self.enemy_index])
        self.state = CombateState.PLAYER_ANIMATION
        self.combat_player.on_animation_ended.append(self.player_animation_ended)

    def player_magic(self):
        self.combat_player.do_magic(self.magic, self.enemies[self.enemy_index])
        self.state = CombateState.PLAYER_ANIMATION
        self.combat_player.on_animation_ended.append(self.player_animation_ended)
        self.magic.start_animating((self.enemies[self.enemy_index].position[0] - self.enemy_size[0] / 4,
                                   self.enemies[self.enemy_index].position[1]))

    def enemy_animation_ended(self):
        self.enemies_turn += 1
        if self.enemies_turn > self.enemies_count:
            self.state = CombateState.IDLE
        else:
            self.state = CombateState.ENEMIES

    def player_animation_ended(self):
        self.enemies_turn = 0
        if self.state != CombateState.ENEMIES_DEAD:
            self.state = CombateState.ENEMIES

    def on_all_enemies_dead(self):
        self.exit_state()
        self.level_name.die()
        Sound.stop_all()


class CombatMenu(pygame.sprite.Sprite):
    sprites = None

    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.position = position
        if CombatMenu.sprites is None:
            path = '../graphics/ui/combat/combat_menu-Sheet.png'
            sheet = SpriteSheet(path)
            CombatMenu.sprites = [pygame.transform.scale(img, (380, 335)) for img in
                                  sheet.load_strip((0, 0, 420, 380), 4, (0, 0, 0))]
        self.sprites = CombatMenu.sprites
        self.animation_frame = 0
        self.animation_speed = .1
        self.image = self.sprites[0]

    def update(self):
        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(self.sprites):
            self.animation_frame = 0
        self.image = self.sprites[int(self.animation_frame)]


class CombateState(Enum):
    CHOOSE_MAGIC = 'choose_magic'
    IDLE = 'idle'
    CHOOSE_ENEMY = 'choose_enemy'
    ENEMIES = 'enemies'
    ENEMIES_DEAD = 'enemies_dead'
    ENEMY_ANIMATION = 'enemy_animation'
    PLAYER_ANIMATION = 'player_animation'
