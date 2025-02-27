import pygame
from game.configManager import ConfigManager
from game.objects.decor.platforms import Platforms

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Door(Platforms):
   def __init__(self, x = 0, y = 0 ):
      self.surf = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/metalicdoor/metalicdoor.PNG")
      super().__init__(x,y,self.surf.get_width(), self.surf.get_height()) 
      self.initial_y = y
      self.on_screen = True
        
   def init_surf(self):
      self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))    
                  
   def switch_position(self):     
      self.rect.y += self.height
   
   def reset_back(self):
      self.rect.y = self.initial_y
        
   def draw(self, screen):
        if self.on_screen:
           screen.blit(self.surf,[self.rect.x, self.rect.y ]) 