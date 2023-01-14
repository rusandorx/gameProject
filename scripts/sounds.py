import pygame


class Sound:
    sounds = []

    def __init__(self, name, time):
        self.sound = pygame.mixer.Sound(name)
        self.sound.play(time)
        self.time = time
        Sound.sounds.append(self.sound)

    def stop(self):
        self.sound.stop()

    def play(self):
        self.sound.play(self.time)

    @staticmethod
    def stop_all():
        for i in Sound.sounds:
            i.stop()
