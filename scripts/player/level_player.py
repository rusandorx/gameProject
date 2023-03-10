from enum import Enum
from sounds import Sound

import pygame


class AnimationState(Enum):
    IDLE = 'idle'
    MOVE_UP = 'up'
    MOVE_DOWN = 'down'
    MOVE_LEFT = 'left'
    MOVE_RIGHT = 'right'


class LevelPlayer(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(*groups)

        # Передвижение
        self.direction = pygame.math.Vector2()
        self.velocity = 5

        # Спрайты
        self.sprites = {AnimationState.MOVE_UP: [pygame.transform.scale(
            pygame.image.load(f'../graphics/player/up/up_{i}.png').convert_alpha(),
            (32, 32))
            for i in range(4)],
            AnimationState.MOVE_DOWN: [
                pygame.transform.scale(
                    pygame.image.load(f'../graphics/player/down/down_{i}.png').convert_alpha(),
                    (32, 32))
                for i in range(4)],
            AnimationState.MOVE_LEFT: [
                pygame.transform.scale(
                    pygame.image.load(f'../graphics/player/left/left_{i}.png').convert_alpha(),
                    (32, 32))
                for i in range(4)],
            AnimationState.MOVE_RIGHT: [
                pygame.transform.scale(
                    pygame.image.load(f'../graphics/player/right/right_{i}.png').convert_alpha(),
                    (32, 32))
                for i in range(4)],
            AnimationState.IDLE: [
                pygame.transform.scale(
                    pygame.image.load('../graphics/player/down/down_0.png').convert_alpha(),
                    (32, 32))]
        }
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.sprite_state: AnimationState = AnimationState.IDLE
        self.image = self.sprites[self.sprite_state][self.animation_frame]

        # Хитбокс и позиция
        self.position = position
        self.obstacle_sprites: pygame.sprite.Group = obstacle_sprites
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-10, -10)
        self.steps = Sound("../sounds/step.mp3", -1)
        self.step_bool = 0

    def update_state(self):
        # Спрайты на движения
        if self.direction.magnitude() == 0:
            self.sprite_state = AnimationState.IDLE
        elif self.direction.y > 0:
            self.sprite_state = AnimationState.MOVE_DOWN
        elif self.direction.y < 0:
            self.sprite_state = AnimationState.MOVE_UP
        elif self.direction.x > 0:
            self.sprite_state = AnimationState.MOVE_RIGHT
        elif self.direction.x < 0:
            self.sprite_state = AnimationState.MOVE_LEFT

    def animate(self):
        sprites = self.sprites[self.sprite_state]

        self.animation_frame += self.animation_speed
        self.animation_frame = 0 if self.animation_frame >= len(sprites) else self.animation_frame

        self.image = sprites[int(self.animation_frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def key_input(self, key_state):
        keys = key_state

        if keys['up']:
            self.direction.y = -1
        elif keys['down']:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys['left']:
            self.direction.x = -1
        elif keys['right']:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, velocity):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            if self.step_bool == 0:
                self.step_bool = 1
                self.steps.play()
        else:
            self.steps.stop()
            self.step_bool = 0


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

    def update(self, key_state=None):
        if key_state is None:
            return
        self.key_input(key_state)
        self.update_state()
        self.animate()
        self.move(self.velocity)
