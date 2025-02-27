import pygame
from game.objects.platforms import Platforms

class Door(Platforms):
   def __init__(self, x = 0, y = 0, width = 0, height = 18 ):
      super().__init__(x,y,width, height)
        
              
   def switch_position(self):
      print("done")