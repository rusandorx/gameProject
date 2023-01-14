import pygame


class Sound:
    def __init__(self, name, time_fadeout):
        s = pygame.mixer.Sound(name)
        s.play()
        pygame.mixer.music.fadeout(time_fadeout)