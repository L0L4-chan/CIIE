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
from game.objects.stone import Stone
vec = pygame.math.Vector2 #2 for two dimensional

class Player(pygame.sprite.Sprite):

    #constructor: requiere las posiciones donde el personaje debe aparecer
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
        self.index = 1 #para ver la siguiente animación
        self.frames = sorted(os.listdir(f"../Art/{self.config.get_artpath()}/skelly/to_right"))
        self.end = len(self.frames) -1
        self.animation_timer = 0  # Temporizador para la animación
        self.frame_rate = 4 #cada cuantos loops cambiamos la animación valor entre 5 y diez no menos
        self.jumpchecked = False #indica si ya se ha comprobado el salto
        self.shooting = False
        
    #funcion que genera el movimiento (maneja tambien el salto y el cambio de imagen)
    def move(self,platforms):
        
        if(self.shooting):
            self.index = 0
            self.shoot()
        else:    
            self.acc = vec(0,0.5)
            pressed_keys = pygame.key.get_pressed()
            self.animation_timer += 1    #aumentamos el tiempo de la animación      
            if pressed_keys[pygame.K_LEFT]: #si se ha pulsado izquierda
                self.acc.x = - self.ACC #cambiamos la aceleración para que cambie la direccion del personaje
                if self.animation_timer > self.frame_rate and not self.jumping: # si han pasado 10 loops al menos y no esta saltando
                    if (not self.direction): #si la direccion no ha cambiado
                        self.get_next("to_left") #movemos la animacion
                    else:
                        self.direction = 0 #cambiamos la direccion
                        self.index = 0 #comenzamos el contador de imagenes
                        self.end = len(self.frames) -1 #calculamos cual es el ultimo frame para generar el loop
                        self.get_next("to_left") # cambiamos la animacion
                else: 
                    self.direction = 0 #o cambiamos la direccion
            if pressed_keys[pygame.K_RIGHT]:
                self.acc.x = self.ACC
                if self.animation_timer > self.frame_rate and not self.jumping :
                    if (self.direction):
                        self.get_next("to_right")
                    else:
                        self.direction = 1
                        self.index = 0
                        self.end = len(self.frames) -1
                        self.get_next("to_right")
                else: 
                    self.direction = 1
            if pressed_keys[pygame.K_UP]:
                    self.jump(platforms)     
             
        #se realizan calculos para determinar la nueva posicion       
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc # se modifica posicion
         
        #si se sale de la pantalla vuelve por el otro lado, esto se debera eliminar o cambiar por la activacion de cambio de pantalla
        if self.pos.x > self.config.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x =  self.config.get_width()
        
        self.rect.midbottom = self.pos #actualiza posiscion del collider
        
    #Funcion que devuelve la siguiente imagen en el ciclo segun el movimiento
    def get_next(self, path): 
        
        self.index += 1
        if self.index > self.end:
            self.index = 1
        self.frame_path = os.path.join(f"../Art/{self.config.get_artpath()}/skelly/{path}", self.frames[self.index])
        self.surf = pygame.image.load(self.frame_path)
        self.animation_timer = 0 
        
    
    #funcion del salto de momento simple maneja tambien el cambio de imagen de la animación
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -10
            if self.animation_timer > self.frame_rate:
                if(self.direction):
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_jump/001.png")
                    self.animation_timer = 0
                else:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_jump/002.png")
                    self.animation_timer = 0  
    
    #posicion de no movimiento
    def rest(self):
        if self.animation_timer > self.frame_rate:
                if(self.direction):
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_right/001.png")
                    self.animation_timer = 0
                else:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_left/001.png")
                    self.animation_timer = 0 
           
    def shoot(self):
        #aumenta el tiempo para avanzar la animacion
        if self.shooting:
            self.animation_timer += 1
            # Seleccionar el directorio de animaciones según la dirección
            shoot_path = "stoneR" if self.direction else "stoneL"
            if self.animation_timer > self.frame_rate:
                if self.index >=2:  # Si se llega al último frame
                    self.shooting = False
                    self.index = 0  # Reiniciar la animación
                    self.rest()
                    # Crear y devolver la piedra después de la animación
                    stone_x = self.pos.x + (self.rect.width * self.direction)
                    stone_y = self.config.get_height() - (self.rect.height) - 18
                    return Stone(x = stone_x, y = stone_y, direction= self.direction)
                else:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/{shoot_path}/{self.frames[self.index]}")
                    self.animation_timer = 0  # Reiniciar el temporizador
                    # Cambiar frame de animación
                    self.index += 1
        
        return None  # No devuelve piedra hasta que termine la animación
               
        
    #evita que se produzca doble salto
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    # realiza las llamadas para la actividad del personaje (varia ciertos valores si el jugador esta tocando suelo (relacionados al salto))
    def update(self, platforms):
        self.move(platforms)
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0:        
            if hits:
                if self.pos.y < hits[0].rect.bottom:         
                    self.pos.y = hits[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                    self.rest()
                    

