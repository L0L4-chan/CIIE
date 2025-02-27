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
from game.base import Base
from game.configManager import ConfigManager
from game.gameManager import GameManager

class GameOver(Base):
  def __init__(self):
    super().__init__()
    self.button = Button (pos=((self.screen_width/2), (self.screen_height/2)), text_input= ConfigManager().get_instance().get_text_button(key ="GAMEOVER"))
    self.bg = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/background/gameover.png")
    self.run()
  
  def handle_events(self): 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
        if self.button.checkForInput(pygame.mouse.get_pos()): 
          self.running = False  # Sale de la pausa y vuelve al juego
          GameManager().get_instance().load_menu()
  
  def cleanup(self):
    #pygame.mixer.music.stop()  
    import gc
    gc.collect()
  
  def update(self):
    mouse_pos = pygame.mouse.get_pos()
    self.button.changeColor(mouse_pos)   

  def render(self):               
    # Dibuja el fondo negro (cambiamos por algo??)
    self.screen.blit(self.bg,(0,0))
    self.button.render(self.screen) # Dibuja el botón
    pygame.display.flip()  # Actualiza la pantalla