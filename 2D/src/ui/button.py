'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

from game.configManager import ConfigManager

class Button():
    #le pasamos posicion y texto
	def __init__(self, pos, text_input):
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.base_color = (255,255,255)
		self.text_input = text_input
		self.text = ConfigManager().get_instance().get_font().render(self.text_input, True, (255,255,255))
		self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

 	#funcion de dibujado en pantalla
	def update(self, screen):
		screen.blit(self.text, self.text_rect)
	#comprueba si hay input, se le pasa la posicion del ratón
	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False
	#cambia de color si elraton esta por encima, se le pasa la posicion del ratón
	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.base_color = (0,200, 0)
		else:
			self.base_color = (255,255,255)	
		self.text = ConfigManager().get_instance().get_font().render(self.text_input, True, self.base_color)