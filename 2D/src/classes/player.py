'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame, os
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional

class Player(pygame.sprite.Sprite):

    #constructor
    def __init__(self, x, y):
        super().__init__()
        self.config = ConfigManager().get_instance()
        self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/skeleton_1.png") # carga de sprite o imagen
        self.rect = self.surf.get_rect() # proporcionamos collider
        self.pos = vec(x,y) # posicion inicial
        self.vel = vec(0,0) # velocidad inicial
        self.ACC = 0.5  #aceleración del movimiento
        self.FRIC = -0.12 # friccion
        self.jumping = False #variable que se usa en caso de doble salto provisional
        self.speed = 5 #velocidad
        self.direction = 1 # uno indica que se mueve a la derecha, 0 si esta caminando hacia la izquierda. 
        self.last_position = vec(0,0)
        self.index = 1 
        self.frames = sorted(os.listdir(f"../Art/{self.config.get_artpath()}/skelly/to_right"))
        self.frame_index = 1
        self.end = len(self.frames) -1
        self.animation_timer = 0  # Temporizador para la animación
        self.frame_rate = 10
        
        
    #funion que genera el movimiento
    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()
        self.animation_timer += 1          
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = - self.ACC
            if self.animation_timer > self.frame_rate:
                if (not self.direction):
                    self.get_next("to_left")
                else:
                    self.direction = 0
                    self.index = 0
                    self.end = len(self.frames) -1
                    self.get_next("to_left")
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.ACC
            if self.animation_timer > self.frame_rate:
                if (self.direction):
                    self.get_next("to_right")
                else:
                    self.direction = 1
                    self.index = 0
                    self.end = len(self.frames) -1
                    self.get_next("to_right")
               
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
         #si se sale de la pantalla vuelve por el otro lado, esto se debera eliminar o cambiar por la activacion de cambio de pantalla
        if self.pos.x > self.config.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x =  self.config.get_width()
             
        self.rect.midbottom = self.pos
    
    def get_next(self, path):
        
        self.index += 1
        if self.index > self.end:
            self.index = 1
        self.frame_path = os.path.join(f"../Art/{self.config.get_artpath()}/skelly/{path}", self.frames[self.index])
        self.surf = pygame.image.load(self.frame_path)
        self.animation_timer = 0 
        
    
    #funcion del salto de momento simple
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -10
 
    #evita que se produzca doble salto
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    #varia ciertos valores si el jugador esta tocando suelo (relacionados al salto)
    def update(self, platforms):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:         
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False

