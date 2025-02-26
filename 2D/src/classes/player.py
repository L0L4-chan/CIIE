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
from game.objects.stone import Stone
from game.objects.heart import Heart
from game.objects.lassoup import LassoUp
from game.objects.lassoside import LassoSide
from game.objects.platforms import Platforms
from game.objects.spikes import Spikes

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width =  ConfigManager().get_instance().get_player_W()
        self.height =  ConfigManager().get_instance().get_player_H()
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/skelly/spritesheet.png") #cargamos la imagen de inicio
        self.surf =  self.spritesheet.subsurface(pygame.Rect(0,0, self.width,self.height))
        self.rect = pygame.Rect(x, y,self.width, self.height) #obtenemos el collisionador
        self.pos = vec(x, y) #posicion de inicio
        self.respawn = self.pos
        self.vel = vec(0, 0) # vector velocidad para los movimientos
        self.local = vec(x,y)
        self.ACC =  ConfigManager().get_instance().get_player_Acc()  # constante aceleracion
        self.FRIC =  ConfigManager().get_instance().get_player_fric() # constante friccion (suaviza el movimiento)
        self.speed =  ConfigManager().get_instance().get_player_speed #velocidad de movimiento
        self.jump_Max = ConfigManager().get_instance().get_player_jump()
        self.y_acc_value =  ConfigManager().get_instance().get_player_Acc()
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height =  ConfigManager().get_instance().get_height()
        self.art_path = ConfigManager().get_instance().get_artpath()
        self.index = 0
        self.level = 5
        self.lifes = 3
        #Bools para manejod e acciones
        self.jumping = False 
        self.shooting = False
        self.pushing = False
        self.lasso_u = False
        self.lasso_s = False
        self.die = False
        self.shield = False 
        self.bombing = False 
        self.direction = 1 # direccion 1 sera derecha y 0 izquierda
        #accedemos a los archivos (abria que cambiarlo si se cambio el numero de archivos pero de momento como solo es necesario para derecha e izquiera y ambos comparten
        # nombre y numero solo se llama una vez)
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación
        self.frames = {
            "idle": [(0, 0)],  # Una sola imagen para idle
            "walk": [( self.width + (i * self.width), 0) for i in range(4)],  # 4 imágenes para caminar
            "jump": [(( self.width* 5), 0)],  # Una sola imagen para salto
            "shoot": [(( self.width* 6 ) + ( i * self.width), 0) for i in range(3)],  # 3 imágenes para disparo
            "bomb": [( self.width * 9 + (i * self.width), 0) for i in range(4)], # 4 para el corazón
            "shield": [(( self.width* 13 ) + ( i * self.width), 0) for i in range(3)], #2 para el escudo
            "lasso_side": [(( self.width* 15 ) + ( i * self.width), 0) for i in range(3)],
            "lasso_up": [(( self.width* 18 ) + ( i *self.width), 0) for i in range(3)],
            "death" :  [(( self.width* 21 ) + ( i *self.width), 0) for i in range(3)],
            "push" :  [(( self.width* 24 ) + ( i *self.width), 0) for i in range(2)],
        
        }
        self.current_action = "idle"  # Acción inicial
        stone_path = f"../Art/{self.art_path}/stone/001.png"
        self.projectiles = Stone(path=stone_path)
        heart_path = f"../Art/{self.art_path}/heart/spritesheet.png"
        self.heart = Heart(heart_path)
        self.bomb_counter = 0
        self.shield_counter = 0
        lasso_side_path = f"../Art/{self.art_path}/bowel/002.png"
        self.lasso_side = LassoSide(lasso_side_path)
        lasso_up_path = f"../Art/{self.art_path}/bowel/001.png"
        self.lasso_up = LassoUp(lasso_up_path)
    
        self.group = pygame.sprite.Group()
        self.group.add(self.projectiles, self.heart, self.lasso_side, self.lasso_up)
    
    def get_pos(self):
        return self.rect.topleft
        
    def get_local(self):
        return self.local 

    def set_local(self,vector):
        self.local = vector
    
    def get_lifes(self):
        return self.lifes

    def handle_idle(self):
        self.acc.x = 0
        self.current_action = "idle"

    def handle_walk_left(self):
        self.acc.x = -self.ACC
        self.direction = 0
        self.current_action = "walk"

    def handle_walk_right(self):
        self.acc.x = self.ACC
        self.direction = 1
        self.current_action = "walk"

    def handle_jump(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = self.jump_Max
        self.current_action = "jump"

    def handle_shoot(self):
        if self.projectiles.get_inUse():
            self.acc.x = 0
            self.current_action = "idle"
        else:
            self.shooting = True
            self.current_action = "shoot"

    def handle_shield(self):
        self.current_action = "shield"
        self.shield = True

    def handle_lasso_up(self):
        self.current_action = "lasso_up"
        self.lasso_u = True

    def handle_lasso_side(self):
        self.current_action = "lasso_side"
        self.lasso_s = True

    def handle_bomb(self):
        self.current_action = "bomb"
        self.bombing = True
        self.index = 0
        self.bomb_counter = 0

    def handle_push(self):
        self.current_action = "push"
        self.index = 0
        self.pushing = True
        self.original_acc = self.acc.x
        self.original_vel = self.vel.x
        self.acc.x /= 2
        self.vel.x /= 2


    def move(self, platforms):
        if not self.shooting and not self.bombing and not self.die:
            self.acc = vec(0, self.y_acc_value)
            pressed_keys = pygame.key.get_pressed()

            action_map = {
                pygame.K_LEFT: self.handle_walk_left,
                pygame.K_RIGHT: self.handle_walk_right,
                pygame.K_SPACE: lambda: self.handle_jump(platforms),
                pygame.K_q: self.handle_shoot,
                pygame.K_a: self.handle_shield if self.level >= 4 else None,
                pygame.K_w: self.handle_lasso_up if self.level >= 2 else None,
                pygame.K_e: self.handle_lasso_side if self.level >= 2 else None,
                pygame.K_s: self.handle_bomb if self.level >= 3 and self.bomb_counter > 300 else None,
                pygame.K_d: self.handle_push,
            }

            if not any(pressed_keys):
                self.handle_idle()
                self.pushing = False
            else:
                for key, action in action_map.items():
                    if pressed_keys[key] and action:
                        action()
                        break

            # Cálculos de posición
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            # Colocamos el collisionador
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
        elif self.current_action == "shield" and self.index >= index -1:
            self.shield = False
            self.shield_counter = 0
            self.current_action= "idle"
            self.index = 0
        elif self.current_action == "bomb" and self.index >= index -1:
            self.bombing = False
            self.explode()
            self.current_action= "idle"
            self.index = 0
        elif self.current_action == "death" and self.index >= index -1:
            if self.lifes >= 0 :
                self.rect.topleft = self.respawn
                self.current_action= "idle"
                self.index = 0
                self.lifes -=1
                self.die = False    
        elif self.current_action == "lasso_up":
            if self.index == 1:
                self.get_lasso("up")
            elif self.index ==  index -1:
                self.index = 0
                print("pendiente escalada")          
        elif self.current_action == "lasso_side" and self.index and self.index == 1:
            if self.index == 1:
                self.get_lasso("side")
            elif self.index ==  index -1:
                self.current_action= "idle"
                self.index = 0
        elif self.current_action == "jump" or self.current_action == "idle" or self.index == index:
            self.index = 0
        frame = action_frames[self.index]
        # Cargamos la imagen del sprite de acuerdo con la acción actual
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], self.width,self.height))
        
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
        stone_y = self.rect.y  + ((self.height) /2)
        self.projectiles.active(x= stone_x, y = stone_y, direction= self.direction) 
    
    def explode(self):
        if(self.direction):
            heart_x = self.pos.x + (self.rect.width * self.direction)
        else:
            heart_x = self.pos.x - (self.rect.width)
        heart_y = self.rect.y + ((self.height) /2)
        self.heart.active(x= int( heart_x), y = int(heart_y), direction= self.direction)
        self.bomb_counter = 0 
    
    def get_lasso(self, position):
        if position == "up":
            if(self.direction):
                lzz_x = self.pos.x + (self.rect.width/6 * self.direction)
            else:
                lzz_x = self.pos.x 
            lzz_y = self.rect.y 
            self.lasso_up.active(x= lzz_x, y = lzz_y, direction= self.direction)  
        else:
            if(self.direction):
                lzz_x = self.pos.x + (self.rect.width/2 * self.direction)
            else:
                lzz_x = self.pos.x - (self.rect.width/2)
            lzz_y = self.rect.y  + ((self.height/6)*4)
            self.lasso_side.active(x= lzz_x, y = lzz_y, direction= self.direction)    
            
    def level_up(self):
        self.level += 1
        if(self.level == 2):
            self.jump_Max *=2
    
    def collision_managment(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False) #comprueba colisiones con las plataformas del suelo, posiblemente requiera modificacion cualdo haya mas
              
        for hit in hits:
            if isinstance(hit, Platforms): 
                if self.vel.y > 0 and self.pos.y < hit.rect.bottom:         
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
            if isinstance(hit, Spikes):
                if not self.die:
                    self.die =  True
                    self.pos.y = hits[0].rect.top + 1 
                    self.current_action = "death"
                    self.animation_timer = self.frame_rate + 1
    
        
    #funcion de actualizacion para ser llamada desde el game loop    
    def update(self, platforms= None):
        self.animation_timer += 1
        self.bomb_counter += 1
        self.shield_counter += 1 
        self.move(platforms) # llama a move para gestionar las entradas del teclado
        self.collision_managment(platforms)
       
        if self.animation_timer > self.frame_rate:
            self.draw()
        #self.projectiles.update(screen) # actualiza los proyectiles en la pantalla se maneja en el game loop de momento
            
