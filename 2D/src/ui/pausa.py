'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''


import pygame, sys,  utils.globals as globals
from game.base import Base
from ui.button import Button

class Pausa(Base):
  def __init__(self):
    """
    Constructor de la clase Pausa.
    """
    super().__init__()
    self.buttons = {
      "back": Button(pos=((self.screen_width/2), (self.screen_height/3)), 
                text_input=  globals.config.get_text_button(key ="BACK"))   ,
      "quit": Button(pos=(self.screen_width /2, self.screen_height/2), 
                text_input= globals.config.get_text_button(key ="QUIT")),
        }  
    self.clock =  globals.game.get_clock()
    self.FPS =  globals.config.get_fps()

  # Manejo de eventos del mouse
  def handle_events(self):
    """
    Manejo de eventos del mouse.
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:   # Detecta si se ha hecho clic sobre el botón "Volver"
        if self.buttons["back"].checkForInput(pygame.mouse.get_pos()): 
          self.buttons["back"].make_sound()
          self.running = False  # Sale de la pausa y vuelve al juego
        if self.buttons["quit"].checkForInput(pygame.mouse.get_pos()):
          self.buttons["quit"].make_sound() 
          self.running = False  # Sale de la pausa y vuelve al juego
          globals.game.load_menu()

  # Actualiza el color de los botones si el ratón está sobre ellos
  def update(self):
    mouse_pos = pygame.mouse.get_pos()
    for btn in self.buttons.values(): #carga botones
      btn.changeColor(mouse_pos)
   
  # Dibuja los botones en la pantalla  
  def render(self):
     # Dibuja el fondo negro (cambiamos por algo??)
    self.screen.fill((0, 0, 0))
    for btn in self.buttons.values(): #carga botones
      btn.render(self.screen)
    pygame.display.flip()  # Actualiza la pantalla
   
  # bucle de actualizacion para no paralizar los ciclos del reloj  
  def run(self):    
    self.running = True
    while self.running:           
      self.clock.tick(self.FPS) # indicamos el numero de frames por segundo
      self.handle_events()
      self.update()
      self.render()      
