'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar, utils.globals as globals

from game.base import Base
from views.scene import Scene
from views.animationPlayer import AnimationPlayer

class Start(Base):

   def __init__(self, path):
      super().__init__()
      self.info = auxiliar.load_json(auxiliar.get_path(f"config/{path}"))
      self.animation = AnimationPlayer(self.info["ani_path"], self.info["ani_start"], self.info["ani_amount"], self.info["ani_event"])
      self.screen_width =  globals.config.get_width()
      self.screen_height =   globals.config.get_height()
     
      
   def music_on(self):
      pygame.mixer.music.stop()
      pygame.mixer.music.load(auxiliar.get_path(self.info["ani_sound"]))
      pygame.mixer.music.play(-1)
      
   def cleanup(self):
      pygame.mixer.music.stop()
      self.running = False 
      if self.animation:
         self.animation = None
      import gc
      gc.collect()

   def run(self):
      self.music_on()
      self.animation.run()
      if self.info["scene_level"] == 5 :
         globals.game.load_credits()
      else:   
         globals.game.load_game(Scene(self.info["scene_bg"], self.info["scene_file"]), self.info["scene_sound"], self.info["scene_level"]  )