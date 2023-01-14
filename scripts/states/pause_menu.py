import pygame

from states.state import State


class PauseMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.menu = pygame.image.load('../graphics/ui/menu.png')
        self.menu_rect = self.menu.get_rect()
        self.menu_rect.center = (self.game.width * .85, self.game.height * .4)
        self.options = {0: 'Party', 1: 'Items', 2: 'Magic', 3: 'Exit'}
        self.index = 0

        self.cursor_image = pygame.image.load('../graphics/ui/cursor.png')
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_offset_y = self.menu_rect.y + 38
        self.cursor_rect.center = (self.menu_rect.x + 10, self.cursor_offset_y)

    def update(self, key_state):
        self.update_cursor(key_state)
        if key_state['confirm']:
            self.confirm_option()
        if key_state['cancel']:
            self.exit_state()
        self.game.reset_keys()

    def render(self, display):
        self.prev_state.render(display)
        display.blit(self.menu, self.menu_rect)
        display.blit(self.cursor_image, self.cursor_rect)

    def update_cursor(self, key_state):
        if key_state['down']:
            self.index = (self.index + 1) % len(self.options)
        elif key_state['up']:
            self.index = (self.index - 1) % len(self.options)
        self.cursor_rect.y = self.cursor_offset_y + (self.index * 32)

    def confirm_option(self):
        option = self.options[self.index]

        # TODO: Implement all options.
        if option == 'Exit':
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()