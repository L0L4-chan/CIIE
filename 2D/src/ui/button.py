import pygame,  utils.globals as globals, utils.auxiliar as auxiliar

class Button():
    def __init__(self, pos, text_input, image_path=None,  hover_image_path=None):
        """
        Constructor de la clase Button.
        
        :param pos: Posición del botón.
        :param text_input: Texto que mostrará el botón.
        :param image_path: Ruta de la imagen del botón.
        :param hover_image_path: Ruta de la imagen del botón al pasar el ratón por encima.
        :return: None
        """
        #Inicialización de variables       
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.base_color = (255, 255, 255)
        self.text_input = text_input
        self.font =  globals.config.get_font_title() 
        self.is_hovering = False  # Estado para saber si el mouse está sobre el botón
        # Cargar imagen normal
        if image_path:
            self.image_icon = pygame.image.load(image_path)
            self.image = self.image_icon
            # Cargar imagen hover
            if hover_image_path:
                self.hover_image = pygame.image.load(hover_image_path)
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        #Creación del texto si es necesario
        else :
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            self.image = None
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("button.wav")))
        self.sound.set_volume(0.3)    

    def render(self, screen):
        """
        Dibuja el botón en pantalla.
        :   param screen: pantalla en la que se dibuja
        """
        if self.image is not None :          
            screen.blit(self.image, self.rect)
        elif self.text:
             screen.blit(self.text, self.text_rect)


    def checkForInput(self, position):
        """
        Comprueba si el ratón está sobre el botón.
        :param position: Posición del ratón.
        :return: True si el ratón está sobre el botón, False en caso contrario.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    #Función que produce un sonido cuando el botón ha sido presionado
    def make_sound(self):
        self.sound.play()

    def update(self, position):
        """
        Actualiza el estado del botón.
        :param position: Posición del ratón.
        """
        if self.image:
            self.changeImage(position)
        else:
            self.changeColor(position)

    def changeColor(self, position):
        """
        Cambia el color del texto del botón si el ratón está sobre él.
        :param position: Posición del ratón.
        """
        if self.checkForInput(position):
            self.base_color = (128,128,128) #gris
        else:
            self.base_color = (255, 255, 255) # Blanco
        self.text = self.font.render(self.text_input, True, self.base_color)
          
    def changeImage(self, position):
        """
        Cambia la imagen del botón si el ratón está sobre él.
        :param position: Posición del ratón.
        """
        if self.checkForInput(position):
            self.image = self.hover_image
        else:
            self.image = self.image_icon
