'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.configManager import ConfigManager
from game.objects.oneuse import OneUse
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Heart(OneUse):
    def __init__(self, path):
        super().__init__(path)
       
        # Definir el tamaño de cada fotograma de la sprite sheet
        self.width = 40
        self.height = 50
        # Cargar la imagen de la sprite sheet del corazón
        self.surf =  self.spritesheet.subsurface(pygame.Rect(0,0, self.width,self.height))
        # Diccionario de animaciones (por ahora solo bomb, pero puedes agregar más como "walk", etc.)
        self.frames = {
            "bomb": [(i * self.width, 0, self.width, self.height) for i in range(4)]  # 4 fotogramas para la animación 'bomb'
        } 
        self.animation_timer = 0  # Medir el tiempo para cambiar la animación
        self.frame_rate = 10  # Cada cuántos frames cambiamos la animación
        self.index = 0  # Índice para las animaciones
        self.direction = 0  # Dirección (0: izquierda, 1: derecha)
        self.image = None  # Imagen actual del sprite (se actualizará con cada fotograma)
        
        # Posición inicial y estado
        self.rect =  pygame.Rect(0, 0, self.width, self.height)
        self.inUse = False
        
        self.vel_y = 0  # Reiniciar velocidad vertical
        self.acc = 0.5  # Aceleración inicial (gravedad)
        
    def active(self,  x, y ,direction):
        self.direction = direction
        super().active(x,y)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.index = 0
        
    def animation(self):
        if self.index < len(self.frames["bomb"]):
            frame_rect = pygame.Rect(self.frames["bomb"][self.index])
            self.image = self.spritesheet.subsurface(frame_rect)
            self.surf = self.image
            self.index += 1
            if self.direction == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_timer = 0
        else:
            self.inUse = False
            
    def update(self, screen, object = None):
        if(self.inUse):
            self.animation_timer += 1
            # Aplicar gravedad acumulativa
            self.vel_y += self.acc  # Aumenta la velocidad con la gravedad
            self.rect.y += self.vel_y  # Aplica la velocidad a la posición
            
            if(self.rect.x > ConfigManager.get_instance().get_width() or (self.rect.x + self.width)<= 0):
                self.inUse = False
            #manejo de collisiones 
            hits = pygame.sprite.spritecollide(self, object, False)
            #if hits.breakable and self.index >= self.frames[self.index]:
            #    hits.to_break() #desaparecera por lo tanto 
            if self.acc > 0:      
                if hits:
                    if self.rect.y + self.height > hits[0].rect.top:  # Si toca la plataforma
                        self.rect.y = hits[0].rect.top - self.height  # Ajustar posición
                        self.acc = 0  # Detener caída
            if self.animation_timer > self.frame_rate:
                self.animation()     
            super().draw(screen)