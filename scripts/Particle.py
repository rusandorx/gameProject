import random

import pygame


class Particle:
    def __init__(self, combat_player):
        self.combat_player = combat_player
        self.particles = []
        for i in range(20):
            self.particles.append([random.randint(self.combat_player.rect.x + 120, self.combat_player.rect.x + 248),
                                   self.combat_player.rect.y + 500, random.randint(0, 5), 0.15])

    def draw(self, surface):
        for j in range(len(self.particles)):
            i = self.particles[j]
            pygame.draw.ellipse(surface, (255, 0, 0), (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 20:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.combat_player.rect.x + 120, self.combat_player.rect.x + 248),
                                   self.combat_player.rect.y + 500, random.randint(0, 5), 0.15]


