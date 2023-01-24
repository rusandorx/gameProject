import pygame


class Sound:
    sounds = []

    def __init__(self, name, time, fadeout=0):
        self.sound = pygame.mixer.Sound(name)
        self.sound.play(time)
        self.time = time
        self.fadeout = fadeout
        Sound.sounds.append(self)

    def stop(self):
        self.sound.stop()

    def play(self):
        self.sound.play(self.time)

    @staticmethod
    def stop_all():
        for i in Sound.sounds:
            if i.fadeout:
                i.sound.fadeout(i.fadeout)
            else:
                i.sound.stop()

    def fadeout(self, time):
        self.sound.fadeout(time)
