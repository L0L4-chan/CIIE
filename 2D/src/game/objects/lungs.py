'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar
import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.prize import Prize

class Lungs(Prize):
    def __init__(self,x,y):
        super().__init__(x,y, "prize/001.png")
        self.sound = pygame.mixer.Sound(auxiliar.get_path(f"{globals.config.get_audiofxpath("PowerUP.wav")}"))
        self.sound.set_volume(0.5)
    