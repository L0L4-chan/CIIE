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


class LassoSide(OneUse):  # Modo 1 (Horizontal)
    def __init__(self, path):
        super().__init__(path)
        self.width = ConfigManager.get_instance().get_lasso_W()  
        self.height = ConfigManager.get_instance().get_lasso_H()  

        self.frames_sizes = [
            (self.width // 4, self.height),  
            (self.width // 2, self.height),  
            (self.width // 4, self.height)   
        ]

        self.frames = {
            "bowel": [pygame.Rect(0, 0,self.width // 4, self.height), 
                      pygame.Rect(self.width //4 , 0,self.width //2 , self.height), 
                      pygame.Rect((self.width //4) * 3 , 0, self.width //4 , self.height) ]
        }

        self.image = self.spritesheet.subsurface(self.frames["bowel"][0])
        self.index = 0
        self.animation_timer = 0
        self.frame_rate = 5  # Cada cuántos frames cambiamos la animación
        self.direction = 0
        
    def active(self, x, y, direction):
        self.direction = direction
        super().active(x, y)
        self.rect = pygame.Rect(x, y , self.width, self.height)
        self.index = 0
        
        
    def animation(self):
        if self.index < len(self.frames["bowel"]):
            frame_rect = pygame.Rect(self.frames["bowel"][self.index])
            self.image = self.spritesheet.subsurface(frame_rect)
            self.index += 1
            if self.direction == 0:
                self.image = pygame.transform.flip( self.image, True, False)
                self.rect = pygame.Rect(self.x_pos - self.image.get_width(), self.y_pos  , self.width, self.height)
            self.animation_timer = 0
        else:
            self.inUse = False
            self.index = 0  

    def update(self, object=None):
        if self.inUse:
            self.animation_timer += 1
            if object is not None:
                hits = pygame.sprite.spritecollide(self, object, False)
                # TODO
            if self.animation_timer > self.frame_rate:
                self.animation() 
