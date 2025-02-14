import pygame
from game.gameManager import GameManager
from game.configManager import ConfigManager

class DialogBox:
    
    def __init__(self, bg_image=None, event = 0):
        self.gameManager = GameManager.get_instance()
        self.config = ConfigManager().get_instance()
        self.dialog = next((d for d in self.gameManager.texts["dialogues"] if d["event"] == event), None)
        self.icon = pygame.image.load(f"../Art/{self.config.get_artpath()}/avatar/{self.dialog["character"]}.png") # Carga el icono del personaje
        if bg_image: # Carga el fondo del cuadro de diálogo
            self.bg_image = pygame.image.load(bg_image)
        else: # Carga el fondo negro
            self.bg_image = pygame.Surface((100, 100))  # Tamaño inicial arbitrario
            self.bg_image.fill((0, 0, 0))  # Color negro
  
        self.width = (self.config.get_width() / 6) * 4 # Ancho del cuadro de diálogo
        self.margin = 20  # Espacio interno
        self.line_height = self.config.get_font_dialog().get_height() + 5  # Altura de cada línea de texto

    def wrap_text(self):
        
        words = self.dialog["text"].split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.config.get_font_dialog().size(test_line)[0] > self.width - (self.margin * 2):
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line

        lines.append(current_line)  # Añadir la última línea
        return lines

    def draw(self):
        
        if not self.dialog:
            print("Dialog not found")
            return  
        
        lines = self.wrap_text()
        height = len(lines) * self.line_height + (self.margin * 2)  # Ajuste altura del cuadro de texto
        
        screen = self.gameManager.screen
        screen_width, screen_height = screen.get_size()
        
        # Posición del cuadro de diálogo 
        box_x = 50
        box_y = 50

        # Dibujar icono del personaje (si existe)
        if self.icon:
            icon_width, icon_height = self.icon.get_size()  # Tamaño del icono
            icon_scaled = pygame.transform.scale(self.icon, (icon_width, icon_height))
            screen.blit(icon_scaled, (box_x, box_y))
            box_x += icon_width
            
        # Dibujar fondo del cuadro de diálogo
        
        bg_scaled = pygame.transform.scale(self.bg_image, (self.width, height))
        self.gameManager.screen.blit(bg_scaled, (box_x, box_y))

        
        # Dibujar texto dentro del cuadro
        text_x = box_x + self.margin   
        text_y = box_y + self.margin

        for line in lines:
            text_surface = self.config.get_font_dialog().render(line, True, (255, 255, 255))
            screen.blit(text_surface, (text_x, text_y))
            text_y += self.line_height  # Mover hacia abajo para la siguiente línea

