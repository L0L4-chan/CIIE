'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.configManager import ConfigManager
#Clase que controla el juego, se encarga de cargar las escenas, cambiarlas, cargar el jugador, la música, etc.
#Implementa el patron Singleton, solo puede haber una instancia de esta clase en todo el juego.
#Implementa el patron Factory, ya que se encarga de crear las escenas y el jugador.
#Implementa el patron Observer, ya que notifica a las escenas cuando se produce un cambio en el juego.  
#Implementa el patron State, ya que se encarga de gestionar los estados del juego.
#Implementa el patron Strategy, ya que se encarga de cargar las escenas y el jugador segun el nivel del juego.
#Implementa el patron Manejador, ya que se encarga de gestionar las escenas y el jugador.

class GameManager():
    #region __new__
    #singleton
    _instance = None
    
    #create and return de instance
    def __new__(cls):
        """
        Crea una única instancia de la clase (Singleton).

        Asegura que solo exista una instancia de GameManager para controlar el juego.

        :return: La instancia única de la clase.
        :rtype: GameManager
        """
        if cls._instance is None:  #check if already is one in place
            cls._instance = super(GameManager, cls).__new__(cls) #create if necessary
            cls._instance._initialized = False  
        return cls._instance
    #endregion

    #region get_instance
    @classmethod
    def get_instance(cls):
        """
        Obtiene la instancia única de la clase.

        Si no existe una instancia, la crea.

        :return: La instancia única de la clase.
        :rtype: GameManager
        """
        if cls._instance is None: 
            cls._instance = GameManager() #create instance  
        return cls._instance
    #endregion

    #region __init__
    def __init__(self):
        """
        Inicializa la clase GameManager.

        Inicializa pygame, establece la configuración, crea la pantalla, crea el reloj del juego, y carga la escena inicial.
        """
        if not self._initialized:
            pygame.mixer.pre_init(44100,16,2,4096) #initialize the mixer (sound)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)
            pygame.mixer.music.set_volume(.3)
            globals.config = ConfigManager()
            globals.config.load_fonts()
            self.screen = pygame.display.set_mode((globals.config.get_width(), globals.config.get_height()))  # screen size default 1280 x 720
            pygame.display.set_caption("Skelly & Soulie") #display name of the game on the edge of the window
            self.clock = pygame.time.Clock() # create a clock
            self._initialized = True # one is all done state is inicialized
            self.scene = None
            self.next_scene = None
            self.player = None
            self.music = False
            self.music_on()
    #endregion
    
    #region first_scene
    def first_scene(self):
        """
        Carga la escena inicial (menú principal).

        Crea una instancia de la clase Menu asignandola a `self.scene`.
        """
        from ui.menu import Menu
        self.scene = Menu()
    #endregion
    
    #region music_on
    def music_on(self):
        """
        Inicia la música de fondo (intro).

        Carga y reproduce la música de intro en bucle.
        """
        if(not self.music):
                pygame.mixer.music.stop()
                pygame.mixer.music.load(auxiliar.get_path(globals.config.get_audiobspath("00-intro.wav")))
                pygame.mixer.music.play(-1)
                self.music = True
   #endregion
   
   #region changeMusic
    def changeMusic(self, path = None):
        """
        Cambia la música de fondo del juego.

        Carga y reproduce la música especificada. Si no se proporciona una ruta, vuelve a la música de intro.

        :param path: La ruta al archivo de música. Si es None, reproduce la música de intro.
        """
        if path is None:
            self.music_on()
        else: 
            pygame.mixer.music.stop()
            pygame.mixer.music.load(auxiliar.get_path(path))
            pygame.mixer.music.play(-1)
            self.music = True
   #endregion
           
    #region change_resolution
    #change the resolution of the screen
    def change_resolution(self):
        """
        Cambia la resolución de la pantalla.

        Ajusta la resolución de la pantalla según la configuración actual.
        """
        self.screen = pygame.display.set_mode((globals.config.get_width(), globals.config.get_height())) 
    #endregion

    #region load_menu
    #functions to load different scenes
    def load_menu(self):
        """
        Carga la escena del menú principal.

        Detiene la escena actual, crea la escena del menú y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop() 
        self.music = False
        from ui.menu import Menu
        self.next_scene =  Menu()
    #endregion
             
    #region load_options
    def load_options(self):
        """
        Carga la escena de opciones.

        Detiene la escena actual, crea la escena de opciones y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop()
        from ui.options import Options
        self.next_scene = Options()
       
    #endregion
    #region load_game
    def load_game(self, scene, sound, level):
        """
        Carga la escena del juego.

        Detiene la escena actual, carga o crea al jugador, crea la escena del juego y la prepara para ser la próxima escena.

        :param scene: La escena del juego.
        :param sound: El sonido del juego.
        :param level: El nivel del juego.
        """
        if self.scene:
            self.scene.stop()
        if self.player == None:    
            self.load_player(level)
        else:
            self.load_player(level, self.player.get_lifes())
        from game.game import Game
        self.next_scene = Game(scene, sound)
    #endregion
        
    #region load_player
    def load_player(self, level, lifes=3):
        """
        Carga al jugador en el juego.

        Carga la clase de jugador correspondiente al nivel.  Si el nivel es diferente, tambien define el numero de vidas.

        :param level: El nivel del juego.
        :param lifes: El número de vidas del jugador.
        """
        if level == 1:
            from classes.player import Player
            self.player = Player(globals.config.get_player_posx(1), globals.config.get_player_posy(1))   
        elif level == 2: 
            from classes.player1 import Player1
            self.player = Player1(globals.config.get_player_posx(2),globals.config.get_player_posy(2),lifes)
        elif level == 3:
            from classes.player2 import Player2
            self.player = Player2(globals.config.get_player_posx(3), globals.config.get_player_posy(3),lifes)
        else:
            from classes.player2 import Player2
            self.player = Player2(globals.config.get_player_posx(4), globals.config.get_player_posy(4),lifes+1)
    #endregion
        
    #region load_loading
    def load_loading(self):
        """
        Carga la escena de carga.

        Detiene la escena actual, crea la escena de carga y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop()
        from ui.load import Load
        self.next_scene =  Load()
    #endregion
        
    #region load_credits
    def load_credits(self):
        """
        Carga la escena de créditos.

        Detiene la escena actual, crea la escena de créditos y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop()
        self.music = False
        from views.credits import Credits
        self.next_scene =  Credits()
    #endregion
         
    #region load_pause
    def load_pause(self):
        """
        Carga la escena de pausa.

        Crea y ejecuta la escena de pausa.
        """
        from ui.pausa import Pausa
        Pausa().run()
    #endregion
                 
    #region end_game
    def end_game(self):
        """
        Carga la escena de fin del juego (game over).

        Detiene la escena actual, destruye al jugador, crea la escena de game over y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop()
        from views.gameOver import GameOver
        self.player = None
        self.music = False
        self.next_scene =  GameOver()
    #endregion
       
    #region load_start
    def load_start(self, path):
        """
        Carga la escena de inicio (splash screen).

        Detiene la escena actual, crea la escena de inicio con una imagen, y la prepara para ser la próxima escena.
        """
        if self.scene:
            self.scene.stop()
            self.music = False
        from views.start import Start
        self.next_scene = Start(path)
    #endregion
         
    #region player_position
    def player_position(self):
        """
        Obtiene la posición del jugador en la pantalla.

        :return: La posición del jugador (midbottom) o None si el jugador no existe.
        :rtype: tuple or None
        """
        if self.player is not None:
            return self.player.rect.midbottom 
        else:
            return None
    #endregion
    
    #region scene_end
    def scene_end(self):
        """
        Detiene la escena actual.

        Llama al método stop de la escena actual.
        """
        self.scene.stop()
    #endregion
        
    #region get_clock
    def get_clock(self):
        """
        Obtiene el reloj del juego.

        :return: El objeto reloj del juego.
        :rtype: pygame.time.Clock
        """
        return self.clock
    #endregion
    
    #region get_player
    def get_player(self):
        """
        Obtiene al jugador.

        :return: El objeto jugador.
        :rtype: Player
        """
        return self.player
    #endregion
    
    #region run
    def run(self):
        """
        Ejecuta el bucle principal del juego.

        Inicia la escena principal y entra en un bucle que gestiona escenas, ejecutando sus bucles y cambiando entre ellas.
        """
        self.first_scene()
        self.music_on()
        while self.scene is not None:
            self.scene.run() #el run de cada escena
            
            # Verificar si la escena terminó
            if not self.scene.get_running():
                self.scene.cleanup()
                
                # Verificar si hay una nueva escena o salir
                if self.next_scene is not None:
                    self.music_on()
                    self.scene = self.next_scene
                    self.next_scene = None
                else:
                    break
    #endregion