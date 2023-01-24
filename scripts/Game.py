import pygame

from player.player import Player
from scripts.settings import WIDTH, HEIGTH, FPS
from sounds import Sound
from states.title import Title


class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = WIDTH, HEIGTH
        self.display = pygame.Surface((WIDTH, HEIGTH))
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.clock = pygame.time.Clock()
        self.running, self.playing = True, True

        self.key_state = {'up': False, 'down': False, 'left': False, 'right': False, 'confirm': False, 'cancel': False,
                          'l': False, 'k': False, 'start': False}
        self.state_stack = []
        self.player = Player()
        self.load_assets()
        self.load_states()
        pygame.display.set_caption('Skeleton Rain')

    def run(self):
        while self.running:
            self.screen.fill((11, 218, 81))
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_a:
                    self.key_state['left'] = True
                if event.key == pygame.K_d:
                    self.key_state['right'] = True
                if event.key == pygame.K_w:
                    self.key_state['up'] = True
                if event.key == pygame.K_s:
                    self.key_state['down'] = True
                if event.key == pygame.K_p:
                    self.key_state['confirm'] = True
                if event.key == pygame.K_o:
                    self.key_state['cancel'] = True
                if event.key == pygame.K_RETURN:
                    self.key_state['start'] = True
                if event.key == pygame.K_l:
                    self.key_state['l'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.key_state['left'] = False
                if event.key == pygame.K_d:
                    self.key_state['right'] = False
                if event.key == pygame.K_w:
                    self.key_state['up'] = False
                if event.key == pygame.K_s:
                    self.key_state['down'] = False
                if event.key == pygame.K_p:
                    self.key_state['confirm'] = False
                if event.key == pygame.K_o:
                    self.key_state['cancel'] = False
                if event.key == pygame.K_RETURN:
                    self.key_state['start'] = False
                if event.key == pygame.K_l:
                    self.key_state['l'] = False

    def update(self):
        self.state_stack[-1].update(self.key_state)

    def render(self):
        self.state_stack[-1].render(self.display)
        self.screen.blit(pygame.transform.scale(self.display, (self.width, self.height)), (0, 0))
        pygame.display.flip()

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        self.font = pygame.font.Font('../graphics/font/nineteen.ttf', 20)
        self.big_font = pygame.font.Font('../graphics/font/p5hatty.ttf', 40)

    def reset_keys(self):
        for key in self.key_state:
            self.key_state[key] = False

    def load_states(self):
        self.title = Title(self)
        self.state_stack.append(self.title)

    def restart(self):
        self.__init__()
        Sound.stop_all()
