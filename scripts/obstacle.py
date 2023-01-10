import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, position, groups, url_image):
        super().__init__(groups)
        self.image = pygame.image.load(url_image).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
