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
        self.width = self.spritesheet.get_width() / 10
        self.height = self.spritesheet.get_height()
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(4)],
            "death": [((self.width * 8) + (i * self.width), 0) for i in range(2)]
        }
        self.current_action = "walk"
        self.animation_timer = 0
        self.frame_rate = 16
        self.index = 0
        self.screen_width = pygame.display.get_surface().get_width()  # Obtener el ancho de la pantalla
        self.move_distance = 0  # Distancia recorrida en una dirección

    def move(self):
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y* self.speed * 5
        self.move_distance += abs(self.vel.x * self.speed)

        if self.move_distance >= 100:
            self.vel.x = -self.vel.x  # Cambiar de dirección
            self.move_distance = 0

        if self.pos.x > self.screen_width - self.rect.width or self.pos.x < 0:
            self.vel.x = -self.vel.x  # Cambiar de dirección en X
        
        if self.pos.y > 300 or self.pos.y < 100:
            self.vel.y = -self.vel.y

        
        self.rect.center = self.pos
        
    def draw(self):
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


    def collision_managment(self, platforms):
        return super().collision_managment(platforms)
    
    def update(self):
        if self.vel.x != 0:
            self.current_action = "walk"
        else:
            self.current_action = "idle"

        self.move()
        self.draw() 
