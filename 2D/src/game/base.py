'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import  utils.globals as globals

class Base():
    #region __init__
    def __init__(self):
        """
        Inicializa la clase Base.

        Establece la pantalla, las dimensiones de la pantalla y la variable running.
        """
        super().__init__()
        self.screen = globals.game.screen
        self.screen_width =  globals.config.get_width()
        self.screen_height =   globals.config.get_height()
        self.running = False
    #endregion
     
    #region stop
    def stop(self):
        """
        Detiene el bucle principal (running se establece a False).
        """
        self.running = False 
    #endregion
    
    #region get_running
    def get_running(self):
        """
        Obtiene el estado del bucle principal.

        :return: True si el bucle está en ejecución, False en caso contrario.
        :rtype: bool
        """
        return self.running
    #endregion
         
    #region cleanup
    def cleanup(Self):
        """
        Se utiliza para liberar recursos al salir.
        En la clase base no hace nada pero se puede sobreescribir en las clases hijas.
        """
        pass
    #endregion
    
    #region handle_events
    def handle_events(self):
        """
        Maneja los eventos.
        En la clase base no hace nada pero se puede sobreescribir en las clases hijas.
        """
        pass
    #endregion
    
    #region update
    def update(self):
        """
        Actualiza el estado del juego.
        En la clase base no hace nada pero se puede sobreescribir en las clases hijas.
        """
        pass
    #endregion
    
    #region render
    def render(self):
        """
        Dibuja los elementos del juego en la pantalla.
        En la clase base no hace nada pero se puede sobreescribir en las clases hijas.
        """
        pass
    #endregion
        
    #region run
    def run(self):
        """
        Ejecuta el bucle principal del juego.

        Inicializa `running` a True, y entra en un bucle while que llama a `handle_events`, `update` y `render`
        hasta que `running` sea False.
        """
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
    #endregion