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
from game.objects.decor.platforms import Platforms

class Breakable(Platforms):
   def __init__(self, x , y ):
      self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/breakable/breakablesheet.png")
      self.width = self.spritesheet.get_width()/5
      self.height = self.spritesheet.get_height()
      self.frames = {"position": [(i * self.width, 0, self.width, self.height) for i in range(5)]}
      super().__init__(x,y, self.width, self.height)
      self.breaking = False
      self.index = 1
      self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
      self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación 
      self.sound = pygame.mixer.Sound("../Sound/FX/17_knock.wav")
   
   def init_surf(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
    
   def start_break(self):
      if self.animation_timer >= self.frame_rate:
         self.surf = self.spritesheet.subsurface(self.frames["position"][self.index][0], self.frames["position"][self.index][1],self.width, self.height)
         self.animation_timer = 0
         self.index += 1
         if self.index == 2:
            self.sound.play()
         if self.index == 5:
            self.kill()
         
   def on_bomb_Collision(self):
      self.breaking = True
   
   def update(self):
      if self.breaking:
         self.animation_timer += 1
         self.start_break()
         
   
   
   def draw(self, screen, position):
        if self.on_screen:
            screen.blit(self.surf,position)