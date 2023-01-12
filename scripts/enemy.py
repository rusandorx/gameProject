import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, groups, player):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load("../graphics/monsters/bamboo/idle/0.png"), (32, 32))
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -5)
        self.player = player
        self.velocity = 1

    def check_hitbox(self):
        vector_player = pygame.math.Vector2(self.player.rect.x, self.player.rect.y)
        vector_enemy = pygame.math.Vector2(self.rect.x, self.rect.y)

        vector = vector_player - vector_enemy
        print(vector)
        if vector.magnitude() <= 150:
            if vector.magnitude() != 0:
                vector = vector.normalize()
            self.hitbox.x += vector.x * self.velocity
            self.hitbox.y += vector.y * self.velocity
            self.rect.center = self.hitbox.center

    def update(self):
        self.check_hitbox()