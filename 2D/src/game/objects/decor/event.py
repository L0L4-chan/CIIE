'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import utils.auxiliar as auxiliar, pygame ,  utils.globals as globals
from game.gameManager import GameManager
from game.objects.decor.platforms import Platforms


#Objeto pensado para la activavión de fin de nivel y cambio de escena
class Event(Platforms):
    def __init__(self, x, y, w, h, path, level):
        """
        Constructor de la clase Event.
        
        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :param w: Ancho del objeto.
        :param h: Alto del objeto.
        :param path: Ruta del archivo de guardado.
        :param level: Nivel del juego.
        :return: None
        """
        super().__init__(x,y,w,h)
        self.path = path
        self.level = level
        self.triggered = False
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("noKey.wav")))  #suena cuando se pisa sin la llave
        self.sound.set_volume(0.5)
          
    def on_collision(self, player):
        """ 
        Función que se ejecuta cuando el jugador colisiona con el objeto.
        """
        if not self.triggered:
            self.triggered = True
            data = {"level": self.level, "player_lifes":player.get_lifes() }
            auxiliar.save_json(auxiliar.get_path(f"../src/save/level_{self.level}.json"), data)
            globals.game.scene.running = False
            globals.game.load_start(self.path)
    
    def no_key(self, life):
        """
        Función que se ejecuta cuando el jugador no tiene la llave
        y se encuentra en el nivel 3.
        """
        if (self.level-1) == 3:
            globals.game.load_player(3, life)
            globals.game.scene_end()
            from views.scene import Scene
            globals.game.load_game(Scene("level3.jpg", "level3.json"), globals.config.get_audiobspath("06-level3.wav"), 3)
           