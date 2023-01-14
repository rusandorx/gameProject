import pygame


class Sound:
    def __init__(self, name, time):
        self.sound = pygame.mixer.Sound(name)
        self.sound.play(time)
        self.time = time

    def stop(self):
        self.sound.stop()

    def play(self):
        self.sound.play(self.time)