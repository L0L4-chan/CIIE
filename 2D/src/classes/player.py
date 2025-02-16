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

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.config = ConfigManager().get_instance() #requerimos el path de la resolucion a utilizar y el ancho de la pantalla
        self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/skeleton_1.png") #cargamos la imagen de inicio
        self.rect = self.surf.get_rect() #obtenemos el collisionador
        self.pos = vec(x, y) #posicion de inicio
        self.vel = vec(0, 0) # vector velocidad para los movimientos
        self.ACC = 0.5  # constante aceleracion
        self.FRIC = -0.12 # constante friccion (suaviza el movimiento)
        self.speed = 5 #velocidad de movimiento
        self.index = 1 #indice para las imagenes
        #Bools para manejod e acciones
        self.jumping = False 
        self.shooting = False
        self.direction = 1 # direccion 1 sera derecha y 0 izquierda
        #accedemos a los archivos (abria que cambiarlo si se cambio el numero de archivos pero de momento como solo es necesario para derecha e izquiera y ambos comparten
        # nombre y numero solo se llama una vez)
        self.frames = sorted(os.listdir(f"../Art/{self.config.get_artpath()}/skelly/to_right"))
        self.end = len(self.frames) - 1 #el indice final para generar el loop en movimiento
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 4 # limite de cada cuantos frames cambiamos la animación
        
        self.projectiles = pygame.sprite.Group()  # Grupo para almacenar piedras disparadas

    #funcion que maneja los movimientos
    def move(self, platforms):
        if self.shooting: 
            self.shoot()
        else:    
            self.acc = vec(0, 0.5)
            pressed_keys = pygame.key.get_pressed()
            self.animation_timer += 1      

            if pressed_keys[pygame.K_LEFT]:  
                self.acc.x = -self.ACC  
                if self.animation_timer > self.frame_rate and not self.jumping:  
                    if not self.direction:
                        self.get_next("to_left")  
                    else:
                        self.direction = 0  
                        self.index = 0  
                        self.end = len(self.frames) - 1  
                        self.get_next("to_left")  
                else: 
                    self.direction = 0  
                    
            if pressed_keys[pygame.K_RIGHT]:
                self.acc.x = self.ACC
                if self.animation_timer > self.frame_rate and not self.jumping:
                    if self.direction:
                        self.get_next("to_right")
                    else:
                        self.direction = 1
                        self.index = 0
                        self.end = len(self.frames) - 1
                        self.get_next("to_right")
                else: 
                    self.direction = 1
            
            if pressed_keys[pygame.K_UP]:
                self.jump(platforms)

            if pressed_keys[pygame.K_SPACE] and not self.shooting:
                self.shooting = True
                self.index = 0
        #calculos de la nueva posicion
        self.acc.x += self.vel.x * self.FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #limite de pantalla se eliminara o cambiara cuando tengamos la pantalla definitiva 
        if self.pos.x > self.config.get_width():
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = self.config.get_width()
        #situamos el collisionador
        self.rect.midbottom = self.pos  

    #funcion que nos cambia la imagen a mostrar, la carga y la asigna a la superficie
    def get_next(self, path): 
        self.index += 1
        if self.index > self.end:
            self.index = 1
        self.frame_path = os.path.join(f"../Art/{self.config.get_artpath()}/skelly/{path}", self.frames[self.index])
        self.surf = pygame.image.load(self.frame_path)
        self.animation_timer = 0 

    #funcion que maneja el salto y sus animaciones
    def jump(self, platforms): 
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -10
            if self.animation_timer > self.frame_rate:
                if self.direction:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_jump/001.png")
                else:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_jump/002.png")
                self.animation_timer = 0  

    #funcion idle(carga la animación de estar parado)
    def rest(self):
        if self.animation_timer > self.frame_rate:
            if self.direction:
                self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_right/001.png")
            else:
                self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/to_left/001.png")
            self.animation_timer = 0  

    #funcion que maneja la animación y generacion de lanzamiento de piedras
    def shoot(self):
        if self.shooting:
            self.animation_timer += 1
            shoot_path = "stoneR" if self.direction else "stoneL"

            if self.animation_timer > self.frame_rate:
                if self.index >= 2:  
                    self.shooting = False
                    self.index = 0
                    self.rest()

                    stone_x = self.pos.x + (self.rect.width * self.direction)
                    stone_y = self.config.get_height() - (self.rect.height) - 18
                    stone_path = f"../Art/{self.config.get_artpath()}/stone/001.png"
                    new_stone = Stone(x=stone_x, y=stone_y, path=stone_path, direction=self.direction)
                    self.projectiles.add(new_stone)  
                else:
                    self.surf = pygame.image.load(f"../Art/{self.config.get_artpath()}/skelly/{shoot_path}/{self.frames[self.index]}")
                    self.animation_timer = 0  
                    self.index += 1
        
    #funcion de actualizacion para ser llamada desde el game loop    
    def update(self, platforms, screen):
        self.move(platforms) # llama a move para gestionar las entradas del teclado
        #self.projectiles.update(screen) # actualiza los proyectiles en la pantalla se maneja en el game loop de momento
        hits = pygame.sprite.spritecollide(self, platforms, False) #comprueba colisiones con las plataformas del suelo, posiblemente requiera modificacion cualdo haya mas
        if self.vel.y > 0:      
            if hits:
                if self.pos.y < hits[0].rect.bottom:         
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
                    self.rest()



