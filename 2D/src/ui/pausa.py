'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame
from ui.button import Button
from game.configManager import ConfigManager

class Pausa():
  def __init__(self, screen):
    super().__init__()
    self.config = ConfigManager().get_instance()
    self.button = Button(pos=((self.config.get_width()/2), (self.config.get_height()/2)), text_input= self.config.get_text_button(key ="BACK"))
    self.running: False
    self.run(screen)

  def run(self, screen):
      self.running = True
      while self.running:
          for event in pygame.event.get():
              if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
                  if self.button.checkForInput(pygame.mouse.get_pos()): 
                      self.running = False  # Sale de la pausa y vuelve al juego

          # Dibuja el fondo negro (cambiamos por algo??)
          screen.fill((0, 0, 0))
          self.button.update(screen=screen) # Dibuja el botón
          pygame.display.flip()  # Actualiza la pantalla