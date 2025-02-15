'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, random
from game.objects.platforms import Platforms

class Stone(Platforms):
    
    #funcion de inicializacion de plataformas (modificar para pasar la altura por parametros cuando se tengan los escenarios)
    def __init__(self, x = 0, y = 0, width = 20,height = 20, path = "../Art/big/stone/001.png", direction = 1 ):
        super().__init__(x,y,width,height, path) 
        if path is None:#si no hay imagen crea un rectangulo
            self.surf = pygame.Surface((width, self.height))
            self.surf.fill((0,0,0))
        
        else:
            self.image = pygame.image.load(path)
            self.surf = pygame.transform.scale(self.image, (width, height))
        
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
        self.speed = 10 * 1 if direction else -8 #no se porque estos son los numeros para que se vean más o menos a la misma velocidad
    
    #funcion de dibujado   
    def update(self, screen):
        self.rect.x += self.speed
        super().update(screen)