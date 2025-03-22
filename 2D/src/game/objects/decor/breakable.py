'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame ,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.decor.platforms import Platforms

class Breakable(Platforms):
   #Funcion de inicializacion delelemento
   def __init__(self, x , y ):
      #cargamos las imagenes y asignamos tamaño de forma dinámica
      self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/breakable/breakablesheet.png"))
      self.width = self.spritesheet.get_width()/5
      self.height = self.spritesheet.get_height()
      #asignamos posiciones para la carga de imagenes que forman la animación
      self.frames = {"position": [(i * self.width, 0, self.width, self.height) for i in range(5)]}
      #constructor de la clase padre
      super().__init__(x,y, self.width, self.height)
      #Variables necesarias para el funcionamiento
      self.breaking = False
      self.index = 1
      self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
      self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación 
      self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("Explosion.wav")))
      self.sound.set_volume(0.5)
   
   #Funcion que establece la image inicial y la posicion inicial con el colisionador
   def init_surf(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
    
   #Funcion de actualización de estado por llamada de reloj    
   def update(self):
      if self.breaking:
         self.animation_timer += 1
         self.start_break()
   
   #dibujado en pantalla       
   def draw(self, screen, position):
        if self.on_screen:
            screen.blit(self.surf,position)
   
   #funciones de manejo de la clase y sus acciones   
    
   #comienza la animación de rotura del bloque         
   def start_break(self):
      if self.animation_timer >= self.frame_rate:
         self.surf = self.spritesheet.subsurface(self.frames["position"][self.index][0], self.frames["position"][self.index][1],self.width, self.height)
         self.animation_timer = 0
         self.index += 1
         if self.index == 2:
            self.sound.play()
         if self.index == 5:
            self.kill()
   
   #acción en collision      
   def on_bomb_Collision(self):
      self.breaking = True