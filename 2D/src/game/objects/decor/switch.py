
'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.globals as globals,  utils.auxiliar as auxiliar
from game.objects.decor.platforms import Platforms
from game.objects.decor.door import Door

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
#Clase ligada a un objeto Door, que al ser activado cambia de posición
#y abre la puerta ligada a él.
# También resetea la posicion de la puerta al estado original una vez
#el tiempo de activación ha pasado.
class Switch(Platforms):
    def __init__(self, x, y, door_x, door_y):
        """
        Constructor de la clase Switch.

        :param x: Posición inicial en X.
        :param y: Posición inicial en Y.
        :param door_x: Posición inicial en X de la puerta ligada.
        :param door_y: Posición inicial en Y de la puerta ligada.
        :return: None
        """
        
        #cargamos las imagenes y asignamos tamaño de forma dinámica
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/pushbutton/boton.PNG"))
        self.width = self.spritesheet.get_width()/2
        self.height = self.spritesheet.get_height()
        #asignamos posiciones para la carga de imagenes que forman la animación
        self.frames = {"position": [(i * self.width, 0, self.width, self.height) for i in range(2)]}
        #constructor de la clase padre
        super().__init__(x,y, self.width, self.height)
        #Variables necesarias para el funcionamiento
        self.time = 1000
        self.counter = 0
        self.door = Door(door_x, door_y)
        self.pressed = False
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("switch.wav")))
        self.sound.set_volume(0.5)
    
    #Funcion que establece la image inicial y la posicion inicial con el colisionador    
    def init_surf(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect = self.surf.get_rect(topleft=(self.x_pos, self.y_pos))
    
    #Funcion de actualización de estado por llamada de reloj       
    def update(self):
        """
        Inicializa la superficie de la plataforma.
        """
        self.counter += 1
        if self.pressed and self.counter >= self.time:
            self.reset()
     
    #dibujado en pantalla           
    def draw(self, screen, position):
        """
        Dibuja la plataforma en pantalla.
        : param screen: pantalla en la que se dibuja
        : param position: posición en la que se dibuja

        """
        if self.on_screen:
            screen.blit(self.surf,position) 
    
    #funciones de manejo de la clase y sus acciones           
    
    #Getter para la puerta ligada al interruptor
    def get_door(self):
        return self.door

    #funcion que controla la animacion de presionado
    def change_position(self):
        if not self.pressed:
            self.sound.play()
            self.surf = self.spritesheet.subsurface(self.frames["position"][1][0], self.frames["position"][1][1],self.width, self.height)   
            self.rect.y += (self.height / 2)
            self.door.switch_position() #cambiamos la posición de la puerta
            self.counter = 0
            self.pressed = True
    
    #Funcion que restablece la posicion original    
    def reset(self):
        self.surf = self.spritesheet.subsurface(self.frames["position"][0][0], self.frames["position"][0][1],self.width, self.height)
        self.rect.y -= (self.height / 2)
        self.door.reset_back() #restablecemos la posición de la puerta
        self.counter = 0
        self.sound.play()
        self.pressed = False