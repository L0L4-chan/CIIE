'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame
from game.configManager import ConfigManager
vec = pygame.math.Vector2 #2 for two dimensional

class Player(pygame.sprite.Sprite):
    #variables
    ACC = 0.5  #aceleración del movimiento
    FRIC = -0.12 # friccion


    #constructor
    def __init__(self, x, y):
        super().__init__()
        self.config = ConfigManager().get_instance()
        self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/skeleton_1.png") # carga de sprite o imagen
        self.rect = self.surf.get_rect() # proporcionamos collider
        self.pos = vec(x,y) # posicion inicial
        self.vel = vec(0,0) # velocidad inicial

        self.jumping = False #variable que se usa en caso de doble salto provisional
        self.speed = 5 #velocidad
        
    #funvion que genera el movimiento
    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()          
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = - self.ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = self.ACC
                 
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
         #si se sale de la pantalla vuelve por el otro lado, esto se debera eliminar o cambiar por la activacion de cambio de pantalla
        if self.pos.x > self.config.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x =  self.config.get_width()
             
        self.rect.midbottom = self.pos
    
    #funcion del salto de momento simple
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
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

