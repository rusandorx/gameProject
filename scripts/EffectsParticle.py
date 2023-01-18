import random

import pygame


class EffectsParticle:
    def __init__(self, entity):
        self.entity = entity
        self.particles = []
        for i in range(150):
            self.particles.append([random.randint(self.entity.rect.x + 130, self.entity.rect.x + 258),
                                   random.randint(self.entity.rect.y + 300,
                                                  self.entity.rect.y + 800), random.randint(0, 5), 0.5,
                                   random.choices((True, False), weights=(.25, .75))[0]])

    def draw_after(self, surface, color):
        for j in range(len(tuple(filter(lambda particle: particle[4], self.particles)))):
            i = self.particles[j]
            pygame.draw.ellipse(surface, color, (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 10:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.entity.rect.x + 130, self.entity.rect.x + 258),
                                     random.randint(self.entity.rect.y + 300,
                                                    self.entity.rect.y + 800), random.randint(0, 5), 0.15, i[4]]

    def draw_before(self, surface, color):
        for j in range(len(tuple(filter(lambda particle: not particle[4], self.particles)))):
            i = self.particles[j]
            pygame.draw.ellipse(surface, color, (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 10:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.entity.rect.x + 130, self.entity.rect.x + 258),
                                     random.randint(self.entity.rect.y + 300,
                                                    self.entity.rect.y + 800), random.randint(0, 5), 0.15, i[4]]
