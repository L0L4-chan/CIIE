'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import utils.auxiliar as auxiliar
from game.gameManager import GameManager
from game.configManager import ConfigManager
from game.base import Base
from views.scene import Scene
from views.animationPlayer import AnimationPlayer
from enemies.devil import Devil

class Start(Base):

   def __init__(self, path):
      super().__init__()
      self.info = auxiliar.load_json(f"../config/{path}")
      self.animation = AnimationPlayer(self.info["ani_path"], self.info["ani_start"], self.info["ani_amount"], self.info["ani_event"])
      self.screen_width = ConfigManager().get_instance().get_width()
      self.screen_height =  ConfigManager().get_instance().get_height()
      #pygame.mixer.music.stop()
      #pygame.mixer.music.load(self.info["ani_sound"])
      #pygame.mixer.music.play()

      
   def cleanup(self):
      #pygame.mixer.music.stop()
      self.running = False 
      if self.animation:
         self.animation = None
      import gc
      gc.collect()

   def run(self):
      #de momento para probar.
      self.animation.run()
      GameManager().get_instance().enemy = Devil(200,200)
      GameManager().get_instance().load_game(Scene(self.info["scene_bg"], self.info["scene_file"]), self.info["scene_sound"], self.info["scene_level"]  )