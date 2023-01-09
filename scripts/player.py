import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.position = position
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-10, -15)
        self.sprites = {"up": [pygame.image.load(f'../graphics/player/up/up_{i}.png').convert_alpha()
                               for i in range(4)],
                        "down": [pygame.image.load(f'../graphics/player/down/down_{i}.png').convert_alpha()
                               for i in range(4)],
                        "left": [pygame.image.load(f'../graphics/player/left/left_{i}.png').convert_alpha()
                               for i in range(4)],
                        "right": [pygame.image.load(f'../graphics/player/right/right_{i}.png').convert_alpha()
                               for i in range(4)]
                        }
        self.i = 0

        self.direction = pygame.math.Vector2()
        self.velocity = 7
        self.obstacle_sprites: pygame.sprite.Group = obstacle_sprites
        self.y1 = 0
        self.x1 = 0
        self.check = ""

    def key_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.y1 -= 1
            if self.y1 <= -10 and self.check == "up":
                self.y1 = 0
                self.i += 1
            elif self.y1 <= -10:
                self.check = "up"
                self.i = 0
            if self.i == 4:
                self.i = 0
            self.image = self.sprites["up"][self.i]
            self.rect = self.image.get_rect(topleft=self.position)
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.y1 += 1
            if self.y1 >= 10 and self.check == "down":
                self.y1 = 0
                self.i += 1
                self.check = "down"
            elif self.y1 >= 10:
                self.check = "down"
                self.i = 0
            if self.i == 4:
                self.i = 0
            self.image = self.sprites["down"][self.i]
            self.rect = self.image.get_rect(topleft=self.position)
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.x1 -= 1
            if self.x1 <= -10 and self.check == "left":
                self.x1 = 0
                self.i += 1
            elif self.x1 <= -10:
                self.check = "left"
                self.i = 0
            if self.i == 4:
                self.i = 0
            self.image = self.sprites["left"][self.i]
            self.rect = self.image.get_rect(topleft=self.position)
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.x1 += 1
            if self.x1 >= 10 and self.check == "right":
                self.x1 = 0
                self.i += 1
                self.check = "right"
            elif self.x1 >= 10:
                self.check = "right"
                self.i = 0
            if self.i == 4:
                self.i = 0
            self.image = self.sprites["right"][self.i]
            self.rect = self.image.get_rect(topleft=self.position)
        else:
            self.direction.x = 0

    def move(self, velocity):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * velocity
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * velocity
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

    def update(self):
        self.key_input()
        self.move(self.velocity)
