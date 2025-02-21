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

class LassoUp(OneUse):  # Modo 0 (Vertical)
    def __init__(self, path):
        super().__init__(path)
        self.width = ConfigManager.get_instance().get_lasso_H()  
        self.height = ConfigManager.get_instance().get_lasso_W()  

        self.frames_sizes = [
            (self.width, self.height // 4),  
            (self.width, self.height // 2),   
        ]

        self.frames = {
            "bowel": [pygame.Rect(0, 0, w, h) for w, h in self.frames_sizes]
        }
        self.surf = self.spritesheet.subsurface(self.frames["bowel"][0])
        self.index = 0
        self.direction = 0
        self.animation_timer = 0
        self.frame_rate = 10  # Cada cuántos frames cambiamos la animación
        
    def active(self, x, y, direction):
        self.direction = direction
        super().active(x, y)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.index = 0


    #pendiente ver como manejar la subida del personaje
    def animation(self):
        if self.index < len(self.frames["bowel"]):
            frame_rect = pygame.Rect(self.frames["bowel"][self.index])
            self.surf = self.spritesheet.subsurface(frame_rect)
             
            if self.direction:
                self.rect = pygame.Rect(self.x_pos, self.y_pos - self.surf.get_height(), self.width, self.height)
            else:
                self.surf = pygame.transform.flip( self.surf, True, False)
                width = round(self.surf.get_width() * 1.5)
                self.rect = pygame.Rect(self.x_pos - width, self.y_pos - self.surf.get_height(), self.width, self.height)
                
            self.index += 1
            self.animation_timer = 0
        else:
            self.inUse = False
            self.index = 0  
              

    def update(self, screen, object=None):
        if self.inUse:
            self.animation_timer += 1
            if object is not None:
                hits = pygame.sprite.spritecollide(self, object, False)
                # pendiente de gestionar collision con superior TODO
            if self.animation_timer > self.frame_rate:
                self.animation() 
            super().draw(screen)

