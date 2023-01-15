import pygame

from states.state import State


class MagicMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.magic_index = 0

    def update(self, key_state):
        pass

    def render(self, display):
        self.prev_state.render(display)
