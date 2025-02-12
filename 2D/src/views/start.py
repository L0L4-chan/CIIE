'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from game.gameManager import GameManager
from views.scene import Scene
from game.platform import Platform
from classes.player import Player
from classes.enemy import Enemy

from game.game import Game

class Start():
     
   stop_motion = []

   def __init__(self):
      super().__init__()
      self.gameManager = GameManager.get_instance()
      # todo get everything ready for the animation



   def run(self):
      #de momento para probar.
      self.gameManager.player = Player(400,300)
      self.gameManager.enemy = Enemy(1,400,300)

      self.gameManager.scene = Game(Scene(background="cementerio.PNG", pt_skin= "Art/varios/Nueva carpeta/Tile_a(7).png"), sound = "Sound/BSO/levels-_2_.wav" )