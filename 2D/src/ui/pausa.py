'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, sys
from gameManager import GameManager

class Pausa():
    def __init__(self):
      super().__init__()
      self.gameManager = GameManager.get_instance()