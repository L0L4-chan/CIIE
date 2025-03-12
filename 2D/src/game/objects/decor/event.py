'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import utils.auxiliar as auxiliar, pygame
from game.gameManager import GameManager
from game.objects.decor.platforms import Platforms



class Event(Platforms):
    def __init__(self, x, y, w, h, path, level):
        super().__init__(x,y,w,h)
        self.path = path
        self.level = level
        self.triggered = False
        self.sound = pygame.mixer.Sound("../Sound/FX/noKey.wav")  #suena cuando se pisa sin la llave
          
    def on_collision(self, player):
        if not self.triggered:
            self.triggered = True
            data = {"level": self.level, "player_lifes":player.get_lifes() }
            auxiliar.save_json(f"save/level_{self.level}.json", data)
            GameManager.get_instance().scene.running = False
            GameManager().get_instance().load_start(self.path)
    
    def no_key(self, life):
        if (self.level-1) == 3:
            GameManager().get_instance().load_player(3, life)
            GameManager().get_instance().scene_end()
            from views.scene import Scene
            GameManager().get_instance().load_game(Scene("level3.jpg", "level3.json"), "../Sound/BSO/levels-_2_.wav", 3)
           