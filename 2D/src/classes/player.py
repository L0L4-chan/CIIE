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
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/skelly/spritesheet.png") #cargamos la imagen de inicio
        self.surf =  self.spritesheet.subsurface(pygame.Rect(0,0, ConfigManager().get_instance().get_player_W(),ConfigManager().get_instance().get_player_H()))
        self.rect = pygame.Rect(x, y, ConfigManager().get_instance().get_player_W(),ConfigManager().get_instance().get_player_H()) #obtenemos el collisionador
        self.pos = vec(x, y) #posicion de inicio
        self.vel = vec(0, 0) # vector velocidad para los movimientos
        self.local = vec(x,y)
        self.ACC = 0.5  # constante aceleracion
        self.FRIC = -0.12 # constante friccion (suaviza el movimiento)
        self.speed = 5 #velocidad de movimiento
        self.index = 0
        self.level = 1
        #Bools para manejod e acciones
        self.jumping = False 
        self.shooting = False
        self.pushing = False
        self.lasso_up = False
        self.lasso_side = False
        self.die = False
        self.shield = False 
        self.bombing = False 
        self.direction = 1 # direccion 1 sera derecha y 0 izquierda
        #accedemos a los archivos (abria que cambiarlo si se cambio el numero de archivos pero de momento como solo es necesario para derecha e izquiera y ambos comparten
        # nombre y numero solo se llama una vez)
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 6 # limite de cada cuantos frames cambiamos la animación
        self.frames = {
            "idle": [(0, 0)],  # Una sola imagen para idle
            "walk": [( ConfigManager().get_instance().get_player_W() + (i * ConfigManager().get_instance().get_player_W()), 0) for i in range(4)],  # 4 imágenes para caminar
            "jump": [(( ConfigManager().get_instance().get_player_W()* 5), 0)],  # Una sola imagen para salto
            "shoot": [(( ConfigManager().get_instance().get_player_W()* 6 ) + ( i * ConfigManager().get_instance().get_player_W()), 0) for i in range(3)],  # 3 imágenes para disparo
        }
        self.current_action = "idle"  # Acción inicial
        stone_path = f"../Art/{ConfigManager().get_instance().get_artpath()}/stone/001.png"
        self.projectiles = Stone(path=stone_path)

    
    def get_pos(self):
        return self.rect.topleft
        
    def get_local(self):
        return self.local 

    def set_local(self,vector):
        self.local = vector


    #funcion que maneja los movimientos
    def move(self, platforms):
        if not self.shooting:     
            self.acc = vec(0, 0.5)
            pressed_keys = pygame.key.get_pressed()     
            if not any(pressed_keys):# No hay teclas presionadas
                self.acc.x = 0
                self.current_action = "idle"
            if pressed_keys[pygame.K_LEFT]:  
                self.acc.x = -self.ACC  
                self.direction = 0
                self.current_action = "walk"          
            if pressed_keys[pygame.K_RIGHT]:
                self.acc.x = self.ACC
                self.direction = 1
                self.current_action = "walk"  
            if pressed_keys[pygame.K_SPACE]:
                hits = pygame.sprite.spritecollide(self, platforms, False)
                if hits and not self.jumping:
                    self.jumping = True
                    self.vel.y = -10
                self.current_action = "jump"  
            if pressed_keys[pygame.K_q]:
                if self.projectiles.get_inUse():
                    self.acc.x = 0
                    self.current_action = "idle"
                else:
                    self.shooting = True
                    self.current_action = "shoot"  
            if pressed_keys[pygame.K_a] and self.level>= 4 :
                self.current_action = "shield"
                self.shield = True 
            if pressed_keys[pygame.K_w] and self.level>= 2 :
                self.current_action = "lasso_up"
                self.lasso_up = True 
            if pressed_keys[pygame.K_e] and self.level>= 2 :
                self.current_action = "lasso_side"
                self.lasso_side = True 
            if pressed_keys[pygame.K_s] and self.level>= 3 :
                self.current_action = "bomb"
                self.bombing = True 
            if pressed_keys[pygame.K_d]:
                self.current_action = "push"
                self.pushing = True
            #calculos de la nueva posicion
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            #limite de pantalla se eliminara o cambiara cuando tengamos la pantalla definitiva 
            if self.pos.x > ConfigManager().get_instance().get_width():
                self.pos.x = 0
            if self.pos.x < 0:
                self.pos.x = ConfigManager().get_instance().get_width()
            #situamos el collisionador
            self.rect.midbottom = self.pos  

    #funcion que nos cambia la imagen a mostrar, la carga y la asigna a la superficie
    def draw(self):
        # Seleccionamos la imagen actual de la animación
        action_frames = self.frames[self.current_action]  # Lista de fotogramas para la acción actual
        index = len(action_frames)  # Determinamos el índice del fotograma
        if self.current_action == "shoot" and self.index >= index -1:
            self.shooting = False
            self.shoot()
            self.current_action= "idle"
            self.index = 0
        elif self.current_action == "jump" or self.current_action == "idle" or self.index == index:
            self.index = 0
        frame = action_frames[self.index]
        # Cargamos la imagen del sprite de acuerdo con la acción actual
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], ConfigManager().get_instance().get_player_W(),ConfigManager().get_instance().get_player_H()))
        
        # Si la dirección es izquierda, reflejamos la imagen
        if self.direction == 0:
            sprite_image = pygame.transform.flip(sprite_image, True, False)
        self.surf = sprite_image
        self.animation_timer = 0
        self.index += 1
        
    #funcion que maneja la generacion de piedras
    def shoot(self):
        if(self.direction):
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = ConfigManager().get_instance().get_height() - (self.rect.height) - 18
        self.projectiles.active(x= stone_x, y = stone_y, direction= self.direction) 
        
    #funcion de actualizacion para ser llamada desde el game loop    
    def update(self, platforms= None):
        self.move(platforms) # llama a move para gestionar las entradas del teclado
        self.animation_timer += 1
        if self.animation_timer > self.frame_rate:
            self.draw()
        #self.projectiles.update(screen) # actualiza los proyectiles en la pantalla se maneja en el game loop de momento
        hits = pygame.sprite.spritecollide(self, platforms, False) #comprueba colisiones con las plataformas del suelo, posiblemente requiera modificacion cualdo haya mas
        if self.vel.y > 0:      
            if hits:
                if self.pos.y < hits[0].rect.bottom:         
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False




