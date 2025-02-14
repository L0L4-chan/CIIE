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
from views.scene import Scene
from views.animationPlayer import AnimationPlayer
from classes.player import Player
from enemies.boss import Boss

from game.game import Game

class Start():

   def __init__(self, path, sound, event):
      super().__init__()
      self.gameManager = GameManager.get_instance()
      self.config = ConfigManager().get_instance()
      self.animation = AnimationPlayer(path = path, start = 100, amount = 1, event = 1)
      
      pygame.mixer.music.stop()
      pygame.mixer.music.load(sound)
      pygame.mixer.music.play()
      
   
   def run(self):
      #de momento para probar.
    
      #self.animation.run()
      self.gameManager.player = Player(400,300)
      self.gameManager.enemy = Boss(400,300)
      self.gameManager.scene = Game(Scene(background="cementerio.PNG", pt_skin= "../Art/varios/Tiles/Tile_a(7).png"), sound = "../Sound/BSO/levels-_2_.wav" )