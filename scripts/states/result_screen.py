import pygame

from sounds import Sound
from states.state import State


class ResultScreen(State):
    def __init__(self, game):
        super().__init__(game)
        self.rectangle = pygame.Surface((self.game.width, self.game.height))
        self.rectangle.set_alpha(128)
        self.rectangle.fill((0, 0, 0))

        self.prev_player_stats = {
            'lvl': self.game.player.lvl,
            'hp': round(self.game.player.max_hp),
            'mp': round(self.game.player.max_mp),
        }
        prev_magic = [m.name for m in self.game.player.magic]
        for stat in self.game.player.stats:
            if stat in ('weaknesses', ):
                continue
            self.prev_player_stats[stat] = round(self.game.player.stats[stat], 2)

        while self.game.player.lvl_point >= self.game.player.lvl_point_up:
            self.game.player.level_up()

        self.cur_player_stats = {
            'lvl': self.game.player.lvl,
            'hp': round(self.game.player.max_hp),
            'mp': round(self.game.player.max_mp),
        }
        cur_magic = [m.name for m in self.game.player.magic]
        for stat in self.game.player.stats:
            if stat in ('weaknesses',):
                continue
            self.cur_player_stats[stat] = round(self.game.player.stats[stat], 2)
        self.new_magic = tuple(filter(lambda cur: cur not in prev_magic, cur_magic))

    def update(self, key_state):
        if key_state['confirm']:
            self.exit_state()
            self.prev_state.exit_state()
            self.prev_state.level_name.die()
            Sound.stop_all()
        self.prev_state.update({k: False for k in key_state})
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.rectangle, (0, 0))
        for i, stat in enumerate(self.prev_player_stats, 1):
            prev_stat, cur_stat = self.prev_player_stats[stat], self.cur_player_stats[stat]

            prev_text_surface = self.game.font.render(
                f'{stat}: {prev_stat} -> ', True, (255, 255, 255))
            text_rect = prev_text_surface.get_rect()
            text_rect.center = (self.game.width / 2, i * 80)
            display.blit(prev_text_surface, text_rect)

            cur_text_surface = self.game.font.render(f'{cur_stat}', True,
                                                     (255, 255, 255) if cur_stat == prev_stat else (32, 192, 32))
            cur_text_rect = cur_text_surface.get_rect()
            cur_text_rect.topleft = text_rect.topright
            display.blit(cur_text_surface, cur_text_rect)
        if self.new_magic:
            text_surface = self.game.big_font.render(f'NEW SKILLS!! : {", ".join(self.new_magic)}', True, (64, 255, 128))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.game.width / 2, len(self.prev_player_stats) * 80 + 80)
            display.blit(text_surface, text_rect)


