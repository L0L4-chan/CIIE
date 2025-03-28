'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.decor.platforms import Platforms

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Door(Platforms):
   def __init__(self, x = 0, y = 0 ):
      """
        Constructor de la clase Door.

        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :return: None
      """
      self.surf = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/metallicdoor/metallicdoor.PNG"))
      super().__init__(x,y,self.surf.get_width(), self.surf.get_height()) 
      self.initial_y = y
      
        
   def init_surf(self):
      """
      Inicializa la superficie de la plataforma.
      """
      self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))    
                  
   def switch_position(self):  
      """
      Cambia la posición de la puerta cuando se activa el switch.
      """   
      self.rect.y -= self.height
   
   def reset_back(self):
      """
      Resetea la posición de la puerta a la original 
      una vez el tiempo del switch finaliza.
      """
      self.rect.y = self.initial_y
        
   def draw(self, screen, position):
      """
      Dibuja la plataforma en pantalla.
      """
      if self.on_screen:
         screen.blit(self.surf,position) 