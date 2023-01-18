import pygame

from states.state import State


class GameOver(State):
    def __init__(self, game):
        super().__init__(game)
        self.load_assets()
        self.fade_velocity = 5

    def load_assets(self):
        path = '../graphics/ui/game_over/game_over.png'
        self.image = pygame.transform.scale(pygame.image.load(path), (self.game.width, self.game.height))

        self.box = pygame.Surface((self.game.width, self.game.height))
        self.box.fill((0, 0, 0))
        self.box.set_alpha(0)

        self.text_surface_1 = self.game.big_font.render('Game Over', True, (255, 255, 255))
        self.text_rect_1 = self.text_surface_1.get_rect()
        self.text_rect_1.center = (self.game.width / 2, self.game.height / 2)

        self.text_surface_2 = self.game.big_font.render('Press [p] to try again', True, (255, 255, 255))
        self.text_rect_2 = self.text_surface_2.get_rect()
        self.text_rect_2.center = (self.text_rect_1.center[0], self.text_rect_1[1] + 60)

        self.alpha = 0

    def update(self, key_state):
        if key_state['confirm']:
            self.game.restart()
        self.alpha = min(self.alpha + self.fade_velocity, 255)
        self.box.set_alpha(self.alpha)
        self.box.blit(self.image, (0, 0))
        self.box.blit(self.text_surface_1, self.text_rect_1)
        self.box.blit(self.text_surface_2, self.text_rect_2)
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.box, (0, 0))

