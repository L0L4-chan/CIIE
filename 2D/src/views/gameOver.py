'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame, utils.globals as globals
from ui.button import Button
from game.base import Base

class GameOver(Base):
  def __init__(self):
    super().__init__()
    self.button = Button (pos=((self.screen_width/2), (self.screen_height/2)), text_input=  globals.config.get_text_button(key ="GAMEOVER"))
    self.bg = pygame.image.load(f"../Art/{ globals.config.get_artpath()}/background/gameover.jpg")

  
  def handle_events(self): 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
        if self.button.checkForInput(pygame.mouse.get_pos()):
          self.button.make_sound() 
          self.running = False  # Sale de la pausa y vuelve al juego
          globals.game.load_menu()
  
  def cleanup(self):
    pygame.mixer.music.stop()  
    self.running = False 
    import gc
    gc.collect()
  
  def update(self):
    mouse_pos = pygame.mouse.get_pos()
    self.button.changeColor(mouse_pos)   

  def render(self):               
    self.screen.blit(self.bg,(0,0))
    self.button.render(self.screen) # Dibuja el botón
    pygame.display.flip()  # Actualiza la pantalla