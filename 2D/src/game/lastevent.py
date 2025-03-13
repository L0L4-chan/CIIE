'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import  utils.globals as globals
from game.objects.decor.event import Event


class LastEvent(Event):
    def __init__(self, x, y, w, h,  path, level):
        super().__init__(x,y,w,h,path, level)
    
    def on_collision(self, player):
        if not self.triggered:
            self.triggered = True
            globals.game.scene.running = False
            globals.game.load_credits()