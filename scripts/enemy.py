import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups, player, name, attack_callback):
        super().__init__(*groups)
        self.on_attack = attack_callback
        size_enemy = {"bamboo": 32,
                      "spirit": 32,
                      "squid": 32,
                      "big_boss": 128,
                      "raccoon": 64}
        attack_sprites = {"bamboo": 1,
                          "spirit": 1,
                          "squid": 1,
                          "big_boss": 4,
                          "raccoon": 4}
        range_attack = {"bamboo": 150,
                          "spirit": 150,
                          "squid": 150,
                          "big_boss": 300,
                          "raccoon": 150}
        self.range_attack = range_attack[name]
        self.size = size_enemy[name]
        self.image = pygame.transform.scale(pygame.image.load(f"../graphics/monsters/{name}/idle/0.png"),
                                            (self.size, self.size))
        self.init_position = Vector2(position)
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
        self.player = player
        self.velocity = 2
        self.sprites = {"MOVE": [
            pygame.transform.scale(pygame.image.load(f'../graphics/monsters/{name}/move/{i}.png').convert_alpha(),
                                   (self.size, self.size))
            for i in range(4)],
            "IDLE": [
                pygame.transform.scale(
                    pygame.image.load(f"../graphics/monsters/{name}/idle/0.png").convert_alpha(),
                    (self.size, self.size))],
            "ATTACK": [
                pygame.transform.scale(pygame.image.load(f'../graphics/monsters/{name}/attack/{i}.png').convert_alpha(),
                                       (self.size, self.size)) for i in range(attack_sprites[name])]
        }
        self.sprites["ATTACK"] += self.sprites["IDLE"]
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.sprite_state = "IDLE"

    def check_hitbox(self):
        vector_player = Vector2(self.player.rect.x, self.player.rect.y)
        vector_enemy = Vector2(self.rect.center)
        cross_vector = vector_player - vector_enemy

        if cross_vector.magnitude() <= self.range_attack // 5:
            self.sprite_state = "ATTACK"
            if int(self.animation_frame) == len(self.sprites[self.sprite_state]) - 1:
                self.on_attack(self)
        elif cross_vector.magnitude() <= self.range_attack:
            self.move_by_vector(cross_vector)
        elif (cross_vector := (self.init_position - vector_enemy)).magnitude() > 1:
            self.move_by_vector(cross_vector)
        else:
            self.sprite_state = "IDLE"

    def move_by_vector(self, vector: Vector2):
        if vector.magnitude() == 0:
            return

        vector = vector.normalize()
        self.hitbox.x += vector.x * self.velocity
        self.hitbox.y += vector.y * self.velocity
        self.rect.center = self.hitbox.center
        self.sprite_state = "MOVE"

    def animation(self):
        if len(self.sprites[self.sprite_state]) <= 1:
            self.image = self.sprites[self.sprite_state][0]
            return

        sprites = self.sprites[self.sprite_state]

        self.animation_frame += self.animation_speed
        self.animation_frame = 0 if self.animation_frame >= len(sprites) else self.animation_frame

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.check_hitbox()
        self.animation()
