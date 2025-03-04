import pygame
from classes.enemy import Enemy
from game.configManager import ConfigManager

vec = pygame.math.Vector2  # 2 for two dimensional

class Devil(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/devil/devil_spritesheet.png")
        self.rect = self.spritesheet.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * 64, 0) for i in range(3)],
        }
        self.current_action = "walk"
        self.animation_timer = 0
        self.frame_rate = 10
        self.index = 0
        self.screen_width = pygame.display.get_surface().get_width()  # Obtener el ancho de la pantalla
        self.move_distance = 0  # Distancia recorrida en una dirección

    def move(self):
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed
        self.move_distance += abs(self.vel.x * self.speed)

        if self.move_distance >= 20:
            self.vel.x = -self.vel.x  # Cambiar de dirección
            self.move_distance = 0  # Reiniciar la distancia recorrida

        self.rect.center = self.pos
        
    def draw(self, surface):
        action_frames = self.frames[self.current_action]
        frame = action_frames[self.index]

        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], 64, 64))

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