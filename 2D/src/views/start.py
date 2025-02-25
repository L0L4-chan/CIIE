'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, os
from game.gameManager import GameManager
from game.configManager import ConfigManager
from game.base import Base
from views.scene import Scene
from views.animationPlayer import AnimationPlayer
from enemies.devil import Devil

class Start(Base):

   def __init__(self, path, sound, event):
      super().__init__()
      self.animation = AnimationPlayer(path = path, start = 100, amount = 1, event = 1)
      self.screen_width = ConfigManager().get_instance().get_width()
      self.screen_height =  ConfigManager().get_instance().get_height()
      pygame.mixer.music.stop()
      pygame.mixer.music.load(sound)
      pygame.mixer.music.play()
      self.run()
      
   def cleanup(self):
      pygame.mixer.music.stop() 

      if self.animation:
         self.animation = None
      import gc
      gc.collect()

   def run(self):
      #de momento para probar.
      #self.animation.run()
      GameManager.get_instance().enemy = Devil(700,300)
      GameManager.get_instance().load_game(Scene(background="level1.jpg", pt_skin= "../Art/varios/Tiles/Tile_a(7).png", file=(f"../Art/{ConfigManager().get_instance().get_artpath()}/levels/level1.json")), sound = "../Sound/BSO/levels-_2_.wav" )