import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position, groups, image):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
