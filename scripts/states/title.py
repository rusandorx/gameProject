from states.level import Level
from states.state import State


class Title(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, key_state):
        if key_state['start']:
            level = Level(self.game)
            level.enter_state()
        self.game.reset_keys()

    def render(self, display):
        display.fill((128, 128, 128))
        self.game.draw_text(display, 'Noname game', (0,0,0), self.game.width / 2, self.game.height / 2)