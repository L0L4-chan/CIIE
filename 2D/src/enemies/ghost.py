import pygame, random
import math
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional

class Ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/ghost/spritesheet.png")
        self.rect = self.spritesheet.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * 65, 0) for i in range(3)],
        }
        self.current_action = "walk"
        self.animation_timer = 0
        self.frame_rate = 10
        self.index = 0
        self.screen_width = pygame.display.get_surface().get_width()  # Obtener el ancho de la pantalla
        self.move_distance = 0  # Distancia recorrida en una dirección

    def move(self):
        # Movimiento del fantasma: se mueve en un patrón sinusoidal en el eje Y
        self.pos.x += self.vel.x * self.speed
        self.pos.y += math.sin(pygame.time.get_ticks() * 0.005) * self.speed * 10

        if self.pos.x > self.screen_width - self.rect.width or self.pos.x < 0:
            self.vel.x = -self.vel.x  # Cambiar de dirección en X

        self.rect.center = self.pos
        
    def draw(self, surface):
        action_frames = self.frames[self.current_action]
        frame = action_frames[self.index]

        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], 60, 50))

        if self.vel.x < 0:
            sprite_image = pygame.transform.flip(sprite_image, True, False)

        self.surf = sprite_image

        self.animation_timer += 1
        if self.animation_timer > self.frame_rate:
            self.index += 1
            if self.index >= len(action_frames):
                self.index = 0
            self.animation_timer = 0

        surface.blit(self.surf, self.rect.topleft)

    def update(self):
        if self.vel.x != 0:
            self.current_action = "walk"
        else:
            self.current_action = "idle"

        self.move()
        self.draw(pygame.display.get_surface())
