import random

import pygame


class Particle:
    def __init__(self, combat_player):
        self.combat_player = combat_player
        self.particles = []
        for i in range(250):
            self.particles.append([random.randint(self.combat_player.rect.x + 120, self.combat_player.rect.x + 248),
                                   random.randint(self.combat_player.rect.y + 300,
                                      self.combat_player.rect.y + 800), random.randint(0, 5), 0.5])

    def draw(self, surface):
        for j in range(len(self.particles)):
            i = self.particles[j]
            pygame.draw.ellipse(surface, (255, 0, 0), (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 10:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.combat_player.rect.x + 120, self.combat_player.rect.x + 248),
                                     random.randint(self.combat_player.rect.y + 300,
                                                    self.combat_player.rect.y + 800), random.randint(0, 5), 0.15]


