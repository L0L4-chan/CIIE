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
from game.objects.decor.platforms import Platforms
from game.event import Event


class LastEvent(Event):
    def __init__(self, x, y, w, h,  path, level):
        super().__init__(x,y,w,h,path, level)
    
    def on_collision(self, player):
        if not self.triggered:
            self.triggered = True
            GameManager.get_instance().scene.running = False
            GameManager.get_instance().load_credits()