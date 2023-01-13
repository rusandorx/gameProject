import sys

import pygame

from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.display = pygame.Surface((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.key_state = {'up': False, 'down': False, 'left': False, 'right': False, 'space': False}

        pygame.display.set_caption('Noname')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((11, 218, 81))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
