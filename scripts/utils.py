import pygame


def get_outline(image, color=(0, 0, 0)):
    rect = image.get_rect()
    mask = pygame.mask.from_surface(image)
    outline = mask.outline()
    outline_image = pygame.Surface(rect.size).convert_alpha()
    outline_image.fill((0, 0, 0, 0))
    for point in outline:
        outline_image.set_at(point, color)
    return outline_image
