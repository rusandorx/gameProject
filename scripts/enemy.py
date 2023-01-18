import pygame
from pygame.math import Vector2
from sounds import Sound


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups, player, name, attack_callback):
        super().__init__(*groups)
        self.on_attack = attack_callback
        size_enemy = {"skeleton": 32,
                      "bamboo": 32,
                      "knight": 32,
                      "squid": 32,
                      "necromancer": 128,
                      "raccoon": 64}
        attack_sprites = {"skeleton": 1,
                          "bamboo": 1,
                          "knight": 1,
                          "squid": 1,
                          "necromancer": 4,
                          "raccoon": 4}
        range_attack = {"skeleton": 150,
                        "bamboo": 150,
                        "knight": 150,
                        "squid": 150,
                        "necromancer": 300,
                        "raccoon": 150}
        move_sprites = {"skeleton": 5,
                        "knight": 5}
        if name in move_sprites:
            move = move_sprites[name]
        else:
            move = 4
        self.alive = True
        self.died_sprite = pygame.image.load("../graphics/bones/bones.png")
        self.range_attack = range_attack[name]
        self.size = size_enemy[name]
        self.image = pygame.transform.scale(pygame.image.load(f"../graphics/monsters/{name}/idle/0.png"),
                                            (self.size, self.size))
        self.init_position = Vector2(position)
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
        self.player = player
        self.velocity = 2
        self.sprites = {"-MOVE": [
            pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'../graphics/monsters/{name}/move/{i}.png').convert_alpha(),
                                   (self.size, self.size)), True, False)
            for i in range(move)],
            "+MOVE": [
                pygame.transform.scale(pygame.image.load(f'../graphics/monsters/{name}/move/{i}.png').convert_alpha(),
                                       (self.size, self.size))
                for i in range(move)],
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
        self.name = name

    def die(self):
        self.alive = False

    def check_hitbox(self):
        if self.alive:
            vector_player = Vector2(self.player.rect.x, self.player.rect.y)
            vector_enemy = Vector2(self.rect.center)
            cross_vector = vector_player - vector_enemy

            if cross_vector.magnitude() <= self.range_attack // 5:
                self.sprite_state = "ATTACK"
                if int(self.animation_frame) == len(self.sprites[self.sprite_state]) - 1:
                    self.on_attack(self.name, self)
                    Sound("../sounds/fighting.mp3", -1, 500)
            elif cross_vector.magnitude() <= self.range_attack:
                self.move_by_vector(cross_vector)
            elif (cross_vector := (self.init_position - vector_enemy)).magnitude() > 1:
                self.move_by_vector(cross_vector)
            else:
                self.sprite_state = "IDLE"
        else:
            vector_player = Vector2(self.player.rect.x, self.player.rect.y)
            vector_enemy = Vector2(self.rect.center)
            cross_vector = vector_player - vector_enemy

            if cross_vector.magnitude() >= 500:
                self.move_by_vector(cross_vector)
                self.alive = True

    def move_by_vector(self, vector: Vector2):
        if vector.magnitude() == 0:
            return

        vector = vector.normalize()
        self.hitbox.x += vector.x * self.velocity
        self.hitbox.y += vector.y * self.velocity
        self.rect.center = self.hitbox.center
        if vector.x * self.velocity <= 0:
            self.sprite_state = "-MOVE"
        else:
            self.sprite_state = "+MOVE"

    def animation(self):
        if self.alive:
            if len(self.sprites[self.sprite_state]) <= 1:
                self.image = self.sprites[self.sprite_state][0]
                return

            sprites = self.sprites[self.sprite_state]

            self.animation_frame += self.animation_speed
            self.animation_frame = 0 if self.animation_frame >= len(sprites) else self.animation_frame

            self.image = sprites[int(self.animation_frame)]
            self.rect = self.image.get_rect(center=self.hitbox.center)
        else:
            self.image = self.died_sprite

    def update(self):
        self.check_hitbox()
        self.animation()
