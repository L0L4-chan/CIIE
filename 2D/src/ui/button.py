import pygame
from game.configManager import ConfigManager

class Button():
    def __init__(self, pos, text_input, image_path=None, scale=1.0, hover_image_path=None, hover_scale=1.0):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.base_color = (255, 255, 255)
        self.text_input = text_input
        self.font = ConfigManager().get_instance().get_font()
        self.image = None
        self.hover_image = None  # Imagen para el estado hover
        self.scale = scale
        self.hover_scale = hover_scale if hover_scale is not None else scale # Usar la misma escala si no se especifica hover_scale
        self.image_path = image_path
        self.hover_image_path = hover_image_path
        self.is_hovering = False  # Estado para saber si el mouse está sobre el botón
        self.sound = pygame.mixer.Sound("../Sound/FX/button.wav")
        # Cargar imagen normal
        if image_path:
            self.image = self.load_and_scale_image(image_path, scale)


        # Cargar imagen hover
        if hover_image_path:
            self.hover_image = self.load_and_scale_image(hover_image_path, self.hover_scale)
        elif image_path:  # Si no hay hover_image_path, pero si image_path, usa la imagen normal como hover
             self.hover_image =  self.image  # En principio se usa la imagen normal, luego se comprueba
        #Si no ha imagen para hover se crea el texto

        if image_path or hover_image_path:
          if self.text_input:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.text_rect =  self.text.get_rect()
          else:
                self.text = None
                self.text_rect = None
          if self.image:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
          else:
            self.rect = self.hover_image.get_rect(center=(self.x_pos, self.y_pos))

        #Creación del texto si es necesario
        elif text_input:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            self.hover_image = None #Si no se  carga ninguna imagen , el hover image es None.
        else:
             raise ValueError("You must provide either text_input or image_path, or both.")



    def load_and_scale_image(self, image_path, scale):
        image = pygame.image.load(image_path)
        if scale != 1.0:
            new_width = int(image.get_width() * scale)
            new_height = int(image.get_height() * scale)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

    def render(self, screen):

        if self.is_hovering and self.hover_image:
            current_image = self.hover_image
        elif self.image:
            current_image = self.image
        else:
            current_image = None

        if current_image:            
            screen.blit(current_image, self.rect)
            if self.text:
              # Centra el texto sobre la imagen
              text_x = self.rect.centerx - self.text_rect.width // 2
              text_y = self.rect.centery + self.text_rect.height + 15
              screen.blit(self.text, (text_x, text_y))  # Usar coordenadas calculadas
        elif self.text:
             screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.sound.play()
            return True
        return False


    def update(self, position):
        """Comprueba si el ratón está sobre el botón y actualiza el estado."""
        self.is_hovering = self.checkForInput(position)
        #Si no tiene imagen se cambia el color, en caso contrario se gestiona en el renderizado
        if not (self.image_path or self.hover_image):
            self.changeColor(position)

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.base_color = (0, 200, 0)  # Verde
        else:
            self.base_color = (255, 255, 255) # Blanco
        if self.text:   # Solo renderiza si existe.
          self.text = self.font.render(self.text_input, True, self.base_color)