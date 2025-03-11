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
from game.objects.stone import Stone

class Fireball(Stone):
     #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self):
        self.path = "fireball/spritesheet.png"
        super().__init__()
        self.width = self.spritesheet.get_width()/7
        self.height = self.spritesheet.get_height()
        self.frames = {
            "bomb": [(i * self.width, 0, self.width, self.height) for i in range(7)]  # 4 fotogramas para la animación 'bomb'
        } 
        self.animation_timer = 0  # Medir el tiempo para cambiar la animación
        self.frame_rate = 120  # Cada cuántos frames cambiamos la animación
        self.direction = 0  # Dirección (0: izquierda, 1: derecha)
        self.image = self.spritesheet.subsurface(self.frames["bomb"][0]) 
        self.vel_y = 0  # Reiniciar velocidad vertical
        #recurso sonido explosión
        self.sound = pygame.mixer.Sound("../Sound/FX/fire.wav")
    
    
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
    
    
    def update(self, object = None):
        if(self.inUse):
            self.rect.y += self.speed
            self.counter -= 1
            if not self.on_screen and self.counter <= 0:
                self.inUse = False
                self.stand_by()
                self.counter = 3