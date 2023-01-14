import pygame

from states.state import State


class Combat(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, key_state):
        pass

    def render(self, surface):
        bg = pygame.image.load('../graphics/Battleground1/Bright/Battleground1.png')
        rect = bg.get_rect()
        surface.blit(bg, rect)
