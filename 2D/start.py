'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame
from gameManager import GameManager
from scene import Scene
from platform import Platform
from player import Player
from game import Game

class Start():
     
   stop_motion = []

   def __init__(self):
      super().__init__()
      self.gameManager = GameManager.get_instance()
      #para la animación inicial antes de pasar al juego


   def run(self):
      #de momento para probar.
      self.gameManager.player = Player(400,300)
      self.gameManager.scene = Game(Scene(background="cementerio.PNG", pt_skin= "Art/varios/Nueva carpeta/Tile_a(7).png"), sound = "Sound/BSO/levels-_2_.wav" )