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


class Event(Platforms):
    def __init__(self, x, y, w, h, path, level):
        super().__init__(x,y,w,h)
        self.path = path
        self.level = level
        self.triggered = False 
          
    def on_collision(self, player):
        if not self.triggered:
            self.triggered = True
            data = {"level": self.level, "player_lifes":player.get_lifes() }
            auxiliar.save_json(f"save/level_{self.level}.json", data)
            GameManager.get_instance().scene.running = False
            GameManager().get_instance().load_start(self.path)