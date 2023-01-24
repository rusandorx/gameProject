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


def draw_text(display, font_name, text, size, pos):
    font = pygame.font.Font(font_name, size)
    surface = font.render(text, True, (0, 0, 0))
    rect = surface.get_rect()
    rect.center = pos
    display.blit(surface, rect)
