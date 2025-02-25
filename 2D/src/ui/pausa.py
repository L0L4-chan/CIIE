'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame
from game.base import Base
from ui.button import Button
from game.configManager import ConfigManager

class Pausa(Base):
  def __init__(self):
    super().__init__()
    self.button = Button(pos=((self.screen_width/2), (self.screen_height()/2)), text_input= ConfigManager().get_instance().get_text_button(key ="BACK"))
    self.run()

  def handle_event(self): 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
        if self.button.checkForInput(pygame.mouse.get_pos()): 
          self.running = False  # Sale de la pausa y vuelve al juego

  def render(self):
     # Dibuja el fondo negro (cambiamos por algo??)
    self.screen.fill((0, 0, 0))
    self.button.update(self.screen) # Dibuja el botón
    pygame.display.flip()  # Actualiza la pantalla
    

          

         