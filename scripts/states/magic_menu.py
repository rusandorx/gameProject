import pygame

from states.state import State


class MagicMenu(State):
    def __init__(self, game, cb):
        super().__init__(game)
        self.cb = cb
        self.rectangle = pygame.Surface((self.game.width, self.game.height))
        self.rectangle.set_alpha(128)
        self.rectangle.fill((0, 0, 0))
        self.options = self.game.player.magic
        self.OPTION_SIZE = (self.game.width, self.game.height / 10)
        self.option_images = self.get_magic_images(self.options)
        self.index = 0
        self.magic_index = 0

    def get_magic_images(self, magics):
        result = []
        for magic in magics:
            new_rect = pygame.Surface((self.game.width, self.game.height / 10))
            new_rect.set_alpha(128)
            new_rect.fill((0, 0, 0))
            new_rect.blit(magic.icon, (0, 0))
            result.append(new_rect)
        return result

    def update(self, key_state):
        self.handle_keys(key_state)
        self.prev_state.update(key_state)

    def render(self, display):
        self.prev_state.render(display)
        for i, image in enumerate(self.option_images):
            display.blit(image, (0, i * self.OPTION_SIZE[1]))
        display.blit(self.rectangle, (0, 0))

    def handle_keys(self, key_state):
        if key_state['down']:
            self.index = (self.index + 1) % len(self.options)
        elif key_state['up']:
            self.index = (self.index - 1) % len(self.options)
        elif key_state['confirm']:
            self.cb(self.index)
            self.exit_state()
