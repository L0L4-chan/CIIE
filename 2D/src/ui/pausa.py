'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame, sys
from game.base import Base
from ui.button import Button
from game.configManager import ConfigManager
from game.gameManager import GameManager

class Pausa(Base):
  def __init__(self):
    super().__init__()
    self.buttons = {
      "back": Button(pos=((self.screen_width/2), (self.screen_height/3)), 
                text_input= ConfigManager().get_instance().get_text_button(key ="BACK"))   ,
      "quit": Button(pos=(self.screen_width /2, self.screen_height/2), 
                text_input=ConfigManager().get_instance().get_text_button(key ="QUIT")),
        }  
    self.clock =  GameManager().get_instance().clock
    self.FPS = ConfigManager().get_instance().get_fps()

  def handle_events(self): 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
        if self.buttons["back"].checkForInput(pygame.mouse.get_pos()): 
           self.running = False  # Sale de la pausa y vuelve al juego
        if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()): 
           self.running = False  # Sale de la pausa y vuelve al juego
           GameManager().get_instance().load_menu()

  def update(self):
    mouse_pos = pygame.mouse.get_pos()
    for btn in self.buttons.values(): #carga botones
      btn.changeColor(mouse_pos)
    
  def render(self):
     # Dibuja el fondo negro (cambiamos por algo??)
    self.screen.fill((0, 0, 0))
    for btn in self.buttons.values(): #carga botones
      btn.render(self.screen)
    pygame.display.flip()  # Actualiza la pantalla
    

  def run(self):    
    self.running = True
    while self.running:           
      self.clock.tick(self.FPS) # indicamos el numero de frames por segundo
      self.handle_events()
      self.update()
      self.render()      

         