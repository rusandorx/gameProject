import pygame
from debug import debug


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups, player):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load("../graphics/monsters/bamboo/idle/0.png"), (32, 32))
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
        self.player = player
        self.velocity = 2
        self.sprites = {"MOVE": [
            pygame.transform.scale(pygame.image.load(f'../graphics/monsters/bamboo/move/{i}.png').convert_alpha(),
                                   (32, 32))
            for i in range(4)],
                        "IDLE": [
                            pygame.transform.scale(
                                pygame.image.load("../graphics/monsters/bamboo/idle/0.png").convert_alpha(),
                                (32, 32))]
                        }
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.sprite_state = "IDLE"

    def check_hitbox(self):
        vector_player = pygame.math.Vector2(self.player.rect.x, self.player.rect.y)
        vector_enemy = pygame.math.Vector2(self.rect.x, self.rect.y)

        vector = vector_player - vector_enemy
        if vector.magnitude() <= 30:
            self.sprite_state = "IDLE"
            self.animation()
        elif vector.magnitude() <= 150:
            if vector.magnitude() != 0:
                vector = vector.normalize()
            debug(vector.x * self.velocity)
            self.hitbox.x += vector.x * self.velocity
            self.hitbox.y += vector.y * self.velocity
            self.rect.center = self.hitbox.center
            self.sprite_state = "MOVE"
            self.animation()

    def animation(self):
        sprites = self.sprites[self.sprite_state]

        self.animation_frame += self.animation_speed
        self.animation_frame = 0 if self.animation_frame >= len(sprites) else self.animation_frame

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.check_hitbox()
