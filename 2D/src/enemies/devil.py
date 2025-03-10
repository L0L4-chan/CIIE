import pygame
from classes.enemy import Enemy
from game.configManager import ConfigManager
from game.objects.stone import Stone

vec = pygame.math.Vector2  # 2 for two dimensional

class Devil(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/devil/devil_spritesheet.png")
        super().__init__(x,y, (self.spritesheet.get_width() /4), self.spritesheet.get_height(), False )
        self.pos = vec(x, y)
        self.vel = vec(1, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = 0.5 
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(4)],
        }
        self.frame_rate = 16
        self.move_distance = 0  # Distancia recorrida en una dirección

        self.frame_rate = 16
        self.projectiles = Stone()
        self.group.add(self.projectiles)
        self.direction = 0

    def move(self):
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed
        self.move_distance += abs(self.vel.x * self.speed)

        if self.move_distance >= 100:
            self.vel.x = -self.vel.x  # Cambiar de dirección
            self.direction = 1 if self.direction == 0 else 0
            self.move_distance = 0  # Reiniciar la distancia recorrida

        self.rect.center = self.pos
        
    def draw(self):
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

    def update(self):
        if self.vel.x != 0:
            self.current_action = "walk"
        else:
            self.current_action = "idle"

        self.move()
        self.draw()
        
        self.projectiles.update(self.group)
    

    def shoot(self):
        if self.direction:
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        self.projectiles.active(x=stone_x, y=stone_y, direction=self.direction)