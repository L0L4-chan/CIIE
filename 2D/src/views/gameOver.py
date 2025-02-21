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
from game.gameManager import GameManager

class GameOver():
  def __init__(self, screen):
    super().__init__()
    self.button = Button(pos=((ConfigManager().get_instance().get_width()/2), (ConfigManager().get_instance().get_height()/2)), text_input= ConfigManager().get_instance().get_text_button(key ="GAMEOVER"))
    self.running: False
    self.run(screen)

  def run(self, screen):
      self.running = True
      while self.running:
          for event in pygame.event.get():
              if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
                  if self.button.checkForInput(pygame.mouse.get_pos()): 
                      GameManager.get_instance().load_menu()
                      self.running = False  # Sale de la pausa y vuelve al juego

          # Dibuja el fondo negro (cambiamos por algo??)
          screen.fill((255, 0, 0))
          self.button.update(screen=screen) # Dibuja el botón
          pygame.display.flip()  # Actualiza la pantalla