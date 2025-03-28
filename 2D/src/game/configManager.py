'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar
#Clase que gestiona la configuración del juego, carga los textos, las fuentes, el idioma, la dificultad, etc.
#Siguiendo el patro Singleton, solo puede haber una instancia de esta clase.
#Se encarga de cargar la configuración, establecer el idioma, la dificultad y otros parámetros iniciales.
#Se encarga de cargar las fuentes de texto, los textos en el idioma seleccionado y los textos de los botones.
#Se encarga de pasar a otras clases los parametros necesarios
#Implementa el patron Gestor de Configuración.
class ConfigManager:
    #region __new__
    _instance = None
    def __new__(cls):
        """
        Crea una única instancia de la clase (Singleton).

        Asegura que solo exista una instancia de ConfigManager.

        :return: La instancia única de la clase.
        :rtype: ConfigManager
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
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
        :rtype: ConfigManager
        """
        if cls._instance is None: 
            cls._instance = ConfigManager() #create instance  
        return cls._instance
    #endregion
    
    #region __init__
    def __init__(self):
        """
        Inicializa la clase ConfigManager.

        Carga la configuración, establece el idioma, la dificultad y otros parámetros iniciales si la clase no se ha inicializado previamente.
        """
        if not self._initialized:
            self.language = "spanish"
            self.difficulty = 2
            self.conf = auxiliar.load_json(auxiliar.get_path("config/1280x720.json"))
            self.change_texts(self.language) # load text on the apropiate language
            self._initialized = True 
            self.fps = 60
    #endregion
    
    #region load_fonts
    def load_fonts(self):
        """
        Carga las fuentes de texto.

        Carga las fuentes desde los archivos especificados.
        """
        self.fonts_titles = pygame.font.Font(auxiliar.get_path("Font/Cryptik/Cryptik.ttf"),  self.conf["lettering"])
        self.fonts_text =  pygame.font.SysFont("arial",self.conf["btn_lettering"])
        self.font_dialog = pygame.font.SysFont("arial", (self.conf["btn_lettering"] // 2))
    #endregion
        

    #region update_config_lang
    #setter
    def update_config_lang(self, language):
        """
        Actualiza el idioma de la configuración.

        :param language: El nuevo idioma.
        """
        self.language = language
        self.change_language(language)
    #endregion
    
    #region update_config_difficulty
    def update_config_difficulty(self, difficulty):
        """
        Actualiza la dificultad de la configuración.

        :param difficulty: La nueva dificultad.
        """
        self.difficulty = difficulty
    #endregion
        
    #region update_config_meassurement
    def update_config_meassurement(self, path):
        """
        Actualiza la configuración de medición.

        Carga una nueva configuración desde un archivo JSON.

        :param path: La ruta al archivo JSON con la nueva configuración.
        """
        self.conf = auxiliar.load_json(auxiliar.get_path(path))
        self.load_fonts()
    #endregion
     
    #region change_texts
    #@param string language
    def change_texts(self, language):
        """
        Carga los textos según el idioma especificado.

        :param language: El idioma a cargar (e.g., "english", "spanish").
        """
        self.texts = auxiliar.load_json(auxiliar.get_path(f"Dialog/{language}.json"))
        self.btn_text = auxiliar.load_json(auxiliar.get_path(f"ButtonText/{language}.json"))
    #endregion
    
    
    #region change_language
    #change the language configuration
    def change_language(self, language):
        """
        Cambia el idioma actual.

        Vuelve a cargar los textos en el idioma especificado.

        :param language: El nuevo idioma.
        """
        self.textos = self.change_texts(language)
    #endregion

    #region get_language
    #getters
    def get_language(self):
        """
        Obtiene el idioma actual.

        :return: El idioma actual.
        :rtype: str
        """
        return self.language
    #endregion
    
    #region get_difficulty
    def get_difficulty(self):
        """
        Obtiene la dificultad actual.

        :return: La dificultad actual.
        :rtype: int
        """
        return self.difficulty
    #endregion
    
    #region get_width
    def get_width(self):
        """
        Obtiene el ancho de la pantalla.

        :return: El ancho de la pantalla.
        :rtype: int
        """
        return self.conf["width"]
    #endregion
    
    #region get_height
    def get_height(self):
        """
        Obtiene la altura de la pantalla.

        :return: La altura de la pantalla.
        :rtype: int
        """
        return self.conf["height"]
    #endregion
    
    #region get_fps
    def get_fps(self):
        """
        Obtiene los FPS (fotogramas por segundo).

        :return: Los FPS configurados.
        :rtype: int
        """
        return self.fps
    #endregion
    
    #region get_artpath
    def get_artpath(self):
        """
        Obtiene la ruta base para los recursos de arte.

        :return: La ruta base para los recursos de arte.
        :rtype: str
        """
        return self.conf["art_path"]
    #endregion
    
    #region get_iconpath
    def get_iconpath(self):
        """
        Obtiene la ruta al icono de la aplicación.

        :return: La ruta al icono.
        :rtype: str
        """
        return self.conf["icon_path"]
    #endregion
    
    #region get_audiofxpath
    def get_audiofxpath(self, name):
        """
        Obtiene la ruta a un archivo de efecto de sonido.

        :param name: El nombre del archivo de sonido.
        :return: La ruta completa al archivo de sonido.
        :rtype: str
        """
        return self.conf["audio_fx_path"] + name
    #endregion
    
    #region get_audiobspath
    def get_audiobspath(self, name):
        """
        Obtiene la ruta a un archivo de música de fondo.

        :param name: El nombre del archivo de música de fondo.
        :return: La ruta completa al archivo de música de fondo.
        :rtype: str
        """
        return self.conf["audio_bs_path"] + name
    #endregion
    
    #region get_font_title
    def get_font_title(self):
        """
        Obtiene la fuente para los títulos.

        :return: La fuente para los títulos.
        :rtype: pygame.font.Font
        """
        return self.fonts_titles
    #endregion
    
    #region get_font_dialog
    def get_font_dialog(self):
        """
        Obtiene la fuente para los diálogos.

        :return: La fuente para los diálogos.
        :rtype: pygame.font.Font
        """
        return self.font_dialog
    #endregion
    
    #region get_font
    def get_font(self):
        """
        Obtiene la fuente para texto general.

        :return: La fuente para texto general.
        :rtype: pygame.font.Font
        """
        return self.fonts_text
    #endregion

    #region get_size_ltt
    def get_size_ltt(self):
        """
        Obtiene el tamaño de la fuente para títulos.

        :return: El tamaño de la fuente para títulos.
        :rtype: int
        """
        return self.conf["lettering"]
    #endregion
    
    #region get_size_btn_ltt
    def get_size_btn_ltt(self):
        """
        Obtiene el tamaño de la fuente para botones.

        :return: El tamaño de la fuente para botones.
        :rtype: int
        """
        return self.conf["btn_lettering"]
    #endregion
    
    #region get_text
    def get_text(self, key):
        """
        Obtiene un texto específico del archivo de idioma.

        :param key: La clave del texto a obtener.
        :return: El texto correspondiente a la clave.
        :rtype: str
        """
        return self.texts[key]
    #endregion
    
    #region get_text_button
    def get_text_button(self, key):
        """
        Obtiene el texto de un botón específico del archivo de idioma.

        :param key: La clave del texto del botón a obtener.
        :return: El texto del botón correspondiente a la clave.
        :rtype: str
        """
        return self.btn_text[key]
    #endregion
    
    #region get_player_Acc
    def get_player_Acc(self):
        """
        Obtiene la aceleración del jugador.

        :return: La aceleración del jugador.
        :rtype: float
        """
        return self.conf["Acc"]
    #endregion
    
    #region get_player_speed
    def get_player_speed(self):
        """
        Obtiene la velocidad del jugador.

        :return: La velocidad del jugador.
        :rtype: float
        """
        return self.conf["speed"]
    #endregion
    
    #region get_player_jump
    def get_player_jump(self):
        """
        Obtiene la fuerza de salto del jugador.

        :return: La fuerza de salto del jugador.
        :rtype: float
        """
        return self.conf["jump"]
    #endregion
    
    #region get_player_fric
    def get_player_fric(self):
        """
        Obtiene la fricción del jugador.

        :return: La fricción del jugador.
        :rtype: float
        """
        return self.conf["fric"]
    #endregion
    
    #region get_player_posx
    def get_player_posx(self, p):
        """
        Obtiene la posición X inicial del jugador para un nivel específico.

        :param p: El número del nivel.
        :return: La posición X inicial del jugador para el nivel.
        :rtype: int
        """
        return self.conf[f"level{p}x"]
    #endregion
    
    #region get_player_posy
    def get_player_posy(self,p):
        """
        Obtiene la posición Y inicial del jugador para un nivel específico.

        :param p: El número del nivel.
        :return: La posición Y inicial del jugador para el nivel.
        :rtype: int
        """
        return self.conf[f"level{p}y"]
    #endregion
    
    #region get_stone_v
    def get_stone_v(self):
        """
        Obtiene la velocidad de las piedras.

        :return: La velocidad de las piedras.
        :rtype: int
        """
        return self.conf["stone"]
    #endregion
    
    #region get_stone_r
    def get_stone_r(self):
        """
        Obtiene la velocidad de retroceso de las piedras.

        :return: La velocidad de retroceso de las piedras.
        :rtype: int
        """
        return self.conf["rev_stone"]
    #endregion