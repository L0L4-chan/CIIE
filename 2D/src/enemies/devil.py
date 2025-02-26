import pygame
from classes.enemy import Enemy
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional
class Devil(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/devil/devil_spritesheet.png")  # Cargar la hoja de sprites
        self.rect = self.spritesheet.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)  # Velocidad inicial
        self.speed = 3 
        self.frames = {
            "idle": [(0, 0)],  # Una imagen para estar quieto
            "walk": [(i * 64, 0) for i in range(3)],  # 3 imágenes para caminar (por ejemplo, de izquierda a derecha)
        }
        self.current_action = "walk"  # Acción inicial
        self.animation_timer = 0  # Temporizador para manejar el cambio de imágenes
        self.frame_rate = 6  # Cada cuántos frames cambia la imagen
        self.index = 0

    def move(self):
        # Si el diablo se está moviendo de izquierda a derecha o de derecha a izquierda
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Rebotar en los límites de la pantalla
        if self.pos.x > self.screen_width - self.rect.width:
            self.vel.x = -self.vel.x  # Cambia la dirección a izquierda
        elif self.pos.x < 0:
            self.vel.x = -self.vel.x  # Cambia la dirección a derecha

        self.rect.center = self.pos
        print(self.rect)
        
    def draw(self):
        # Seleccionamos la imagen actual de la animación
        action_frames = self.frames[self.current_action]  # Lista de fotogramas para la acción actual
        frame = action_frames[self.index]  # Obtenemos el fotograma actual

        # Cargamos la imagen del sprite de acuerdo con la acción actual
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], 64, 64))  # Usamos el tamaño de los fotogramas (64x64 por ejemplo)

        # Si la dirección es izquierda, reflejamos la imagen
        if self.vel.x < 0:  # Si se mueve hacia la izquierda
            sprite_image = pygame.transform.flip(sprite_image, True, False)

        # Establecer la superficie para dibujar
        self.surf = sprite_image

        # Actualizamos el temporizador de la animación
        self.animation_timer += 1
        if self.animation_timer > self.frame_rate:
            self.index += 1
            if self.index >= len(action_frames):
                self.index = 0  # Volver al principio de la animación si se ha acabado
            self.animation_timer = 0

    def update(self):
        # Cambiar la acción de la animación dependiendo del movimiento del diablo
        if self.vel.x != 0:  # Si el diablo se está moviendo
            self.current_action = "walk"
        else:  # Si el diablo está quieto
            self.current_action = "idle"

        # Actualizar el movimiento y la animación
        self.move()
        self.draw()