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
        self.ACC = 0.5  # constante aceleracion
        self.FRIC = -0.12 # constante friccion (suaviza el movimiento)
        self.speed = 5 #velocidad de movimiento
        self.index = 0
        #Bools para manejod e acciones
        self.jumping = False 
        self.shooting = False
        self.idle = True
        self.direction = 1 # direccion 1 sera derecha y 0 izquierda
        #accedemos a los archivos (abria que cambiarlo si se cambio el numero de archivos pero de momento como solo es necesario para derecha e izquiera y ambos comparten
        # nombre y numero solo se llama una vez)
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación
        self.frames = {
            "idle": [(0, 0)],  # Una sola imagen para idle
            "walk": [( ConfigManager().get_instance().get_player_W() + (i * ConfigManager().get_instance().get_player_W()), 0) for i in range(4)],  # 4 imágenes para caminar
            "jump": [(( ConfigManager().get_instance().get_player_W()* 5), 0)],  # Una sola imagen para salto
            "shoot": [(( ConfigManager().get_instance().get_player_W()* 6 ) + ( i * ConfigManager().get_instance().get_player_W()), 0) for i in range(3)],  # 3 imágenes para disparo
        }
        self.current_action = "idle"  # Acción inicial
        self.projectiles = pygame.sprite.Group()  # Grupo para almacenar piedras disparadas

    #funcion que maneja los movimientos
    def move(self, platforms):
        if not self.shooting:     
            self.acc = vec(0, 0.5)
            pressed_keys = pygame.key.get_pressed()     
            if not any(pressed_keys):# No hay teclas presionadas
                self.idle = True
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
            if pressed_keys[pygame.K_UP]:
                hits = pygame.sprite.spritecollide(self, platforms, False)
                if hits and not self.jumping:
                    self.jumping = True
                    self.vel.y = -10
                self.current_action = "jump"  
            if pressed_keys[pygame.K_SPACE]:
                self.shooting = True
                self.current_action = "shoot"  
                
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
        stone_x = self.pos.x + (self.rect.width * self.direction)
        stone_y = ConfigManager().get_instance().get_height() - (self.rect.height) - 18
        stone_path = f"../Art/{ConfigManager().get_instance().get_artpath()}/stone/001.png"
        new_stone = Stone(x=stone_x, y=stone_y, path=stone_path, direction=self.direction)
        self.projectiles.add(new_stone)  
        
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




