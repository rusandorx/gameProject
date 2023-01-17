from enum import Enum
from math import pi
from random import randint

import pygame

from enemies import enemies, CombatEnemy
from player.combat_player import CombatPlayer
from sounds import Sound
from spritesheet import SpriteSheet
from states.item_menu import ItemMenu
from states.magic_menu import MagicMenu
from states.result_screen import ResultScreen
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
        self.combat_menu = CombateMenu((0, 0))
        self.confirm_buttons = pygame.image.load('../graphics/ui/combat/confirm_button.png')
        self.confirm_buttons_rect = self.confirm_buttons.get_rect()

        self.combat_player = CombatPlayer((200, 400), self.game.player)
        self.main_group.add(self.combat_player)
        self.magic = None
        self.item = None
        self.current_animation = None

        self.enemies_count = randint(*count_enemy)
        self.enemies: [CombatEnemy] = [
            enemies[enemy_name]((self.game.width * 5 / 6 - _ * 256, 400 + 25 * randint(-2, 2)), self.combat_player)
            for _ in
            range(self.enemies_count)]
        self.enemy_size = self.enemies[0].image.get_rect()[2:]
        self.main_group.add(self.enemies)
        self.enemy_index = self.enemies_count - 1
        self.enemies_turn = 0

        self.state = CombateState.IDLE
        self.action = CombateState.IDLE
        self.actions = {
            'attack': self.player_attack,
            'magic': self.player_magic,
            'item': self.player_item
        }
        self.outline = False

    def update(self, key_state):
        if self.magic and self.magic.animating:
            self.magic.update()
        if all(magic.cost > self.combat_player.player.mp for magic in self.combat_player.player.magic):
            self.combat_menu.set_show_magic(False)
        else:
            self.combat_menu.set_show_magic(True)
        self.update_enemies()
        if self.combat_player.player.hp <= 0:
            self.combat_player.on_animation_end.append(self.game.load_states)
        if self.state != CombateState.ANIMATION:
            if self.state == CombateState.ENEMIES:
                if self.enemies_turn >= self.enemies_count:
                    self.state = CombateState.IDLE
                else:
                    self.enemies[self.enemies_turn].random_action()

                    self.set_current_animation(self.enemies[self.enemies_turn], [self.enemy_animation_ended])
            else:
                if self.state != CombateState.CHOOSE_MAGIC:
                    self.handle_keys(key_state)

        self.game.reset_keys()
        self.main_group.update()
        self.combat_menu.update()

    def update_enemies(self):
        rest_enemies = []
        for enemy in self.enemies:
            if not enemy.active:
                continue
            if enemy.dead and enemy.sprite_state != 'die':
                self.game.player.lvl_point += enemy.stats["xp"]
                enemy.die()
                self.set_current_animation(enemy, [])
                continue
            rest_enemies.append(enemy)
        rest_enemies_count = len(rest_enemies)
        if rest_enemies_count == 0:
            if self.state != CombateState.ANIMATION:
                self.set_current_animation(self.enemies[0], [self.on_all_enemies_dead])
        elif rest_enemies_count != self.enemies_count:
            self.enemies = rest_enemies
            self.enemies_count = rest_enemies_count
            self.enemy_index = self.enemies_count - 1

    def render(self, surface):
        surface.blit(self.background, self.background_rect)
        for i in self.enemies:
            if not i.dead:
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
        self.main_group.draw(surface)

        if self.magic and self.magic.animating:
            surface.blit(self.magic.image, self.magic.pos)

        if self.state == CombateState.IDLE:
            surface.blit(self.combat_menu.image,
                         (self.combat_player.position[0], self.combat_player.position[1] - 50))

        if self.outline and self.state == CombateState.CHOOSE_ENEMY and len(self.enemies) > 1:
            surface.blit(self.outline, (self.enemies[self.enemy_index].position[0] - self.enemy_size[0] * .5,
                                        self.enemies[self.enemy_index].position[1] - self.enemy_size[1] * .5))

        if self.state == CombateState.CHOOSE_ENEMY and self.enemies_count > 1:
            surface.blit(self.confirm_buttons, (
                self.game.width - self.confirm_buttons_rect[2], self.game.height - self.confirm_buttons_rect[3]))

    def handle_keys(self, key_state):
        if self.state == CombateState.IDLE:
            if key_state['confirm']:
                self.action = 'attack'
                self.state = CombateState.CHOOSE_ENEMY
            elif key_state['l']:
                # self.action = 'magic'
                if any(magic.cost <= self.combat_player.player.mp for magic in self.combat_player.player.magic):
                    self.state = CombateState.CHOOSE_MAGIC
                    magic_menu = MagicMenu(self.game, self.get_magic_index)
                    magic_menu.enter_state()
            elif key_state['cancel']:
                # self.action = 'item'
                item_menu = ItemMenu(self.game, self.get_item_index)
                item_menu.enter_state()
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
        self.set_current_animation(self.combat_player, [self.player_animation_ended])

    def player_magic(self):
        self.magic.use(self.combat_player, self.enemies[self.enemy_index])
        self.set_current_animation(self.magic, [self.player_animation_ended])
        self.magic.start_animating((self.enemies[self.enemy_index].position[0] - self.enemy_size[0] / 4,
                                    self.enemies[self.enemy_index].position[1]))

    def player_item(self):
        self.item.use(self.combat_player, self.enemies[self.enemy_index])

    def player_animation_ended(self):
        self.enemies_turn = 0
        if self.state != CombateState.ENEMIES_DEAD:
            self.state = CombateState.ENEMIES

    def enemy_animation_ended(self):
        self.enemies_turn += 1
        if self.enemies_turn > self.enemies_count:
            self.state = CombateState.IDLE
        else:
            self.state = CombateState.ENEMIES

    def magic_animation_ended(self):
        pass

    def set_current_animation(self, current_animation, cbs):
        self.state = CombateState.ANIMATION
        self.current_animation = current_animation
        for cb in cbs:
            self.current_animation.on_animation_end.append(cb)

    def get_magic_index(self, index):
        if index == -1:
            self.state = CombateState.IDLE
            self.action = CombateState.IDLE
            return
        self.action = 'magic'
        self.magic = self.game.player.magic[index]
        if self.magic.need_target:
            self.state = CombateState.CHOOSE_ENEMY
        else:
            self.player_magic()

    def get_item_index(self, item):
        if item == -1:
            self.state = CombateState.IDLE
            self.action = CombateState.IDLE
            return
        self.action = 'item'
        self.item = item
        if item.need_target:
            self.state = CombateState.CHOOSE_ENEMY
        else:
            self.player_item()

    def on_all_enemies_dead(self):
        results_screen = ResultScreen(self.game)
        results_screen.enter_state()


class CombateMenu(pygame.sprite.Sprite):
    sprites = None

    def __init__(self, position, *groups):
        super().__init__(*groups)
        self.position = position
        if CombateMenu.sprites is None:
            path = '../graphics/ui/combat/'
            sheet = SpriteSheet(path + 'combat_menu-Sheet.png')
            sheet_without_magic = SpriteSheet(path + 'combat_menu_magic_disabled-Sheet.png')
            CombateMenu.sprites = {'normal': [pygame.transform.scale(img, (380, 335)) for img in
                                   sheet.load_strip((0, 0, 420, 380), 4, (0, 0, 0))],
                                   'no_magic': [pygame.transform.scale(img, (380, 335)) for img in
                                   sheet_without_magic.load_strip((0, 0, 420, 380), 4, (0, 0, 0))]}
        self.sprites = CombateMenu.sprites
        self.animation_frame = 0
        self.animation_speed = .1
        self.state = 'normal'
        self.image = self.sprites[self.state][0]

    def update(self):
        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(self.sprites[self.state]):
            self.animation_frame = 0
        self.image = self.sprites[self.state][int(self.animation_frame)]

    def set_show_magic(self, show_magic):
        if not show_magic:
            self.state = 'no_magic'
            self.animation_speed = .05
            return
        self.state = 'normal'
        self.animation_speed = .1



class CombateState(Enum):
    CHOOSE_MAGIC = 'choose_magic'
    IDLE = 'idle'
    CHOOSE_ENEMY = 'choose_enemy'
    ENEMIES = 'enemies'
    ENEMIES_DEAD = 'enemies_dead'
    ANIMATION = 'animation'
