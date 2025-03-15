'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar
from game.objects.decor.breakable import Breakable
from game.objects.decor.platforms import Platforms
from game.objects.oneuse import OneUse
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Heart(OneUse):
    def __init__(self):
        super().__init__("heart/spritesheet.png")
        # Definir el tamaño de cada fotograma de la sprite sheet
        self.width = self.spritesheet.get_width()/4
        self.height = self.spritesheet.get_height()
        # Diccionario de animaciones 
        self.frames = {
            "bomb": [(i * self.width, 0, self.width, self.height) for i in range(4)]  # 4 fotogramas para la animación 'bomb'
        } 
        self.animation_timer = 0  # Medir el tiempo para cambiar la animación
        self.frame_rate = 10  # Cada cuántos frames cambiamos la animación
        self.direction = 0  # Dirección (0: izquierda, 1: derecha)
        self.image = self.spritesheet.subsurface(self.frames["bomb"][0]) 
        self.vel_y = 0  # Reiniciar velocidad vertical
        #recurso sonido explosión
        self.platform = pygame.sprite.Group()
        self.sound = pygame.mixer.Sound(auxiliar.get_path("../Sound/FX/Explosion.wav"))
        self.sound.set_volume(0.5)
    
    def set_Platform(self,platform):
        self.platform = platform
    
    #funcion que lo activa para reutilización    
    def active(self,  x, y ,direction):
        self.direction = direction
        super().active(x,y, direction)#posicion
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.index = 0
        super().set_use()#activación
        self.acc = 0.5
        
    #funcion que controla los cambios de la animación   
    def animation(self):
        if self.index < len(self.frames["bomb"]):
            frame_rect = pygame.Rect(self.frames["bomb"][self.index])
            self.image = self.spritesheet.subsurface(frame_rect)
            self.index += 1
            if self.direction == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_timer = 0
        else:
            self.sound.play
            super().set_use()
            
    def stand_by(self): 
        self.rect.topleft = (-100, -100)  # La sacamos de la pantalla
        self.speed = 0
            
    def update(self,):
        if(self.inUse):
            self.animation_timer += 1
            self.vel_y += self.acc  # Aumenta la velocidad con la gravedad
            self.rect.y += self.vel_y  # Aplica la velocidad a la posición
            #manejo de collisiones 
            hits = pygame.sprite.spritecollide(self,self.platform, False)
            #if isInstace(hit, Breakable)>= self.frames[self.index]:
            #    hits.to_break() #desaparecera por lo tanto 
            if self.acc > 0:      
                for hit in hits:
                    if isinstance(hit, Platforms):
                        if self.rect.y + self.height > hit.rect.top:  # Si toca la plataforma
                            self.rect.y = hit.rect.top - self.height  # Ajustar posición
                            self.acc = 0  # Detener caída
                    if isinstance(hit, Breakable):
                        hit.on_bomb_Collision()  
            if self.animation_timer > self.frame_rate:
                self.animation()     
        else:
            self.stand_by()