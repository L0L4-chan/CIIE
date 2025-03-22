
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
from game.objects.lungs import Lungs
from game.objects.extra import Extra
from game.objects.key import Key


vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Chest(Platforms):
    def __init__(self, x, y, prize):
        #cargamos las imagenes y asignamos tamaño de forma dinámica
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/chest/chest.png"))
        self.width = self.spritesheet.get_width()/4
        self.height = self.spritesheet.get_height()
        #asignamos posiciones para la carga de imagenes que forman la animación
        self.frames = {"position": [(i * self.width, 0, self.width, self.height) for i in range(4)]}
        super().__init__(x,y, self.width, self.height)
        #Variables necesarias para el funcionamiento
        self.prize = self.set_prize(x,y,prize)
        self.active = True
        self.discovered = False
        self.index = 1
        self.respawn_time = 3000
        self.respaw_x = x
        self.respaw_y = y
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación 
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("OpenChest.wav")))
        self.sound.set_volume(0.5)
     
    #Funcion que establece la image inicial y la posicion inicial con el colisionador
    def init_surf(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
 
    #Funcion de actualización de estado por llamada de reloj         
    def update(self):
       if self.discovered and self.active:
           self.animation_timer += 1
           self.on_discover()
       if self.discovered and not self.active: 
                self.respawn_time -=1
                if not isinstance(self.prize, Key):
                  self.check_respawn()
                  self.index = 0
       
    def check_respawn(self):
        if self.respawn_time <=0:
            self.respawn_time = 3000
            self.discovered = False
            self.index = 0
            self.active = True
            self.init_surf() 
            self.prize.active(self.x_pos, self.y_pos, 1)
 
        
    #dibujado en pantalla       
    def draw(self, screen, position):
        if self.on_screen and self.active:
            screen.blit(self.surf,position) 
    
    #funciones de manejo de la clase y sus acciones 
    
    #devuelve el contenido del cofre          
    def get_prize(self):
        return self.prize
    
    #Coloca el contenido del cofre
    def set_prize(self,x,y, prize):
        if prize == "lungs":
            return Lungs(x,y)
        elif prize == "life":
            return Extra(x,y)
        else:
            return Key(x,y)
    
    #acciones a realizar en collision
    def on_discover(self):
        if self.active and self.animation_timer >= self.frame_rate:
            self.surf = self.spritesheet.subsurface(self.frames["position"][self.index][0], self.frames["position"][self.index][1],self.width, self.height)
            self.animation_timer = 0
            self.index += 1
        if self.index == 4:
            self.sound.play
            self.active = False
            self.prize.set_use()
            self.rect.topleft = (-100, -100)        
    
    #se asegura de que solo se abre una vez
    def open(self):
        if not self.discovered:
            self.discovered = True
            return self.get_prize()
        return None