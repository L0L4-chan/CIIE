'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, random

class Platforms(pygame.sprite.Sprite):
    
    #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self, x = 0, y = 0, width = 0, height = 18, path = None ):
        super().__init__() 

        self.height = height
        self.x_pos = x
        self.y_pos = y
        if width == 0:
            width = random.randint(50, 120)

        if path is None:#si no hay imagen crea un rectangulo
            self.surf = pygame.Surface((width, self.height))
            self.surf.fill((255,0,0))
        
        else:
            self.image = pygame.image.load(path)
            self.surf = pygame.transform.scale(self.image, (width, self.height))
        
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
        
     #funcion de dibujado   
    def update(self, screen):
	    screen.blit(self.surf,self.rect.topleft) 
       

        
 
    