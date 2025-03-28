import pygame, utils.globals as globals, utils.auxiliar as auxiliar

class DialogBox:
    
    def __init__(self, event = 0):
        """
        Constructor de la clase DialogBox.
        
        :param event: Número del dialogo.
        :return: None
        """
        self.screen = globals.game.screen
        self.dialog = next((d for d in globals.config.get_text(key="dialogues") if d["event"] == event), None)
        name = self.dialog["character"]
        self.icon = pygame.image.load(auxiliar.get_path(f"{globals.config.get_artpath()}/avatar/{name}.png")) # Carga el icono del personaje
        self.bg_image = pygame.image.load(auxiliar.get_path(f"{globals.config.get_artpath()}/varios/dialog.png" ))
        self.width = (globals.config.get_width() / 6) * 4 # Ancho del cuadro de diálogo
        self.margin = 20  # Espacio interno
        self.line_height = globals.config.get_font_dialog().get_height() + 5  # Altura de cada línea de texto

        self.font =  globals.config.get_font_dialog()

    # Dividir el texto para que entre en el espacio del cuadro
    def wrap_text(self):
        
        words = self.dialog["text"].split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] > self.width - (self.margin * 2):
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line

        lines.append(current_line)  # Añadir la última línea
        return lines

    # Dibujar el cuadro de diálogo
    def draw(self):
        
        if not self.dialog:
            print("Dialog not found")
            return  
        
        lines = self.wrap_text()
        height = len(lines) * self.line_height + (self.margin * 2)  # Ajuste altura del cuadro de texto
        
        # Posición del cuadro de diálogo 
        box_x = 50
        box_y = 50

        # Dibujar icono del personaje (si existe)
        if self.icon:
            icon_width, icon_height = self.icon.get_size()  # Tamaño del icono
            icon_scaled = pygame.transform.scale(self.icon, (icon_width, icon_height))
            self.screen.blit(icon_scaled, (box_x, box_y))
            box_x += icon_width
            
        # Dibujar fondo del cuadro de diálogo
        
        bg_scaled = pygame.transform.scale(self.bg_image, (self.width, height))
        self.screen.blit(bg_scaled, (box_x, box_y))

        
        # Dibujar texto dentro del cuadro
        text_x = box_x + self.margin   
        text_y = box_y + self.margin

        for line in lines:
            text_surface = self.font.render(line, True, (0,0,0))
            self.screen.blit(text_surface, (text_x, text_y))
            text_y += self.line_height  # Mover hacia abajo para la siguiente línea

