import random

import pygame


class EffectsParticle:
    def __init__(self, entity, offset=(-10, 110), width=80, height=100):
        self.entity = entity
        self.particles = []
        self.colors = []
        self.offset = offset
        self.width, self.height = width, height
        for i in range(150):
            self.particles.append([random.randint(self.entity.rect.center[0] - self.width // 2 + self.offset[0],
                                                  self.entity.rect.center[0] + self.width // 2 + self.offset[0] + self.width),
                                   random.randint(self.entity.rect.center[1] - self.height // 2 + self.offset[1],
                                                  self.entity.rect.center[1] + self.height // 2 + self.offset[1] + self.height),
                                   random.randint(0, 5), 0.5,
                                   random.choices((True, False), weights=(.25, .75))[0], (0, 0, 0)])

    def set_colors(self, colors):
        if all(color in colors for color in self.colors) and all(color in self.colors for color in colors):
            return
        self.colors = colors
        for i in range(len(self.particles)):
            self.particles[i][5] = random.choice(colors)

    def draw_after(self, surface):
        for j in range(len(tuple(filter(lambda particle: particle[4], self.particles)))):
            i = self.particles[j]
            pygame.draw.ellipse(surface, i[5], (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 10:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.entity.rect.center[0] - self.width // 2 + self.offset[0],
                                                  self.entity.rect.center[0] + self.width // 2+ self.offset[0] + self.width),
                                   random.randint(self.entity.rect.center[1] - self.height // 2 + self.offset[1],
                                                  self.entity.rect.center[1] + self.height // 2 + self.offset[1] + self.height),
                                     random.randint(0, 5), 0.15, i[4], i[5]]

    def draw_before(self, surface):
        for j in range(len(tuple(filter(lambda particle: not particle[4], self.particles)))):
            i = self.particles[j]
            pygame.draw.ellipse(surface, i[5], (i[0], i[1], i[2], i[2]))
            i[2] += i[3]
            i[1] -= 1
            if i[2] >= 10:
                i[3] *= -1
            if i[2] <= 0:
                self.particles[j] = [random.randint(self.entity.rect.center[0] - self.width // 2 + self.offset[0],
                                                  self.entity.rect.center[0] + self.width // 2 + self.offset[0] + self.width),
                                   random.randint(self.entity.rect.center[1] - self.height // 2 + self.offset[1],
                                                  self.entity.rect.center[1] + self.height // 2 + self.offset[1] + self.height),
                                     random.randint(0, 5), 0.15, i[4], i[5]]
