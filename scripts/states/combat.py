import pygame

from player.combat_player import CombatPlayer
from states.state import State


class Combat(State):
    def __init__(self, game):
        super().__init__(game)
        self.main_group = pygame.sprite.Group()
        self.background = pygame.image.load('../graphics/Battleground1/Bright/Battleground1.png')
        self.background_rect = self.background.get_rect()
        self.player_sprite = CombatPlayer((180, 400))
        self.main_group.add(self.player_sprite)

        self.menu_image = pygame.transform.scale(pygame.image.load('../graphics/ui/combat/combat_menu.png'), (256, 256))

    def update(self, key_state):
        if key_state['confirm'] and self.player_sprite.sprite_state == 'idle':
            self.player_sprite.attack()
        self.game.reset_keys()
        self.main_group.update()

    def render(self, surface):
        surface.blit(self.background, self.background_rect)
        self.main_group.draw(surface)

    def player_attack(self):
        pass
