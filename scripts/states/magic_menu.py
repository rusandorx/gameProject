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
        self.OPTION_SIZE = (self.game.width, self.game.height / 8)
        self.option_images = self.get_magic_images(self.options)
        self.index = 0
        self.magic_index = 0

    def get_magic_images(self, magics):
        result = []
        for magic in magics:
            padding_x = 10
            padding_y = 10

            new_rect = pygame.Surface(self.OPTION_SIZE)
            new_rect.set_alpha(128)
            new_rect.fill((0, 0, 0))
            new_rect.blit(magic.icon, (padding_x, padding_y))

            text_surface = self.game.font.render(f'{magic.name}', True, (255, 255, 255))
            name_text_rect = text_surface.get_rect()
            name_text_rect.topleft = (64 + padding_x + 10, padding_y)
            new_rect.blit(text_surface, name_text_rect)

            if magic.cost > self.game.player.mp:
                text_surface = self.game.font.render(f'{str(magic.cost)}', True, (255, 0, 0))
            else:
                text_surface = self.game.font.render(f'{str(magic.cost)}', True, (32, 128, 255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (name_text_rect.topright[0] + 10, name_text_rect.topright[1])
            new_rect.blit(text_surface, text_rect)

            text_surface = self.game.font.render(f'{magic.description}', True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (64 + padding_x + 10, 24 + padding_y)
            new_rect.blit(text_surface, text_rect)

            text_surface = self.game.font.render(f'{magic.damage_type}', True, (255, 128, 64))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (64 + padding_x + 10, 48 + padding_y)
            new_rect.blit(text_surface, text_rect)

            result.append(new_rect)
        return result

    def update(self, key_state):
        self.handle_keys(key_state)
        self.prev_state.update(key_state)

    def render(self, display):
        self.prev_state.render(display)
        for i, image in enumerate(self.option_images):
            if i == self.index:
                image.set_alpha(255)
            else:
                image.set_alpha(128)
            display.blit(image, (0, i * self.OPTION_SIZE[1]))
        display.blit(self.rectangle, (0, 0))
        if len(self.game.state_stack) == 4:
            display.blit(self.prev_state.confirm_buttons, (
                self.game.width - self.prev_state.confirm_buttons_rect[2],
                self.game.height - self.prev_state.confirm_buttons_rect[3]))

        text_surface = self.game.font.render(f'{self.game.player.mp}\\{self.game.player.max_mp}', True, (32, 128, 255))
        text_rect = text_surface.get_rect()
        text_rect.topright = (self.OPTION_SIZE[0], 0)
        display.blit(text_surface, text_rect)

    def handle_keys(self, key_state):
        if key_state['down']:
            self.index = (self.index + 1) % len(self.options)
            while self.options[self.index].cost > self.game.player.mp:
                self.index = (self.index + 1) % len(self.options)
        elif key_state['up']:
            self.index = (self.index - 1) % len(self.options)
            while self.options[self.index].cost > self.game.player.mp:
                self.index = (self.index - 1) % len(self.options)
        elif key_state['confirm']:
            self.cb(self.index)
            self.exit_state()
        elif key_state['cancel']:
            self.cb(-1)
            self.exit_state()
        self.game.reset_keys()

