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
from game.objects.decor.platforms import Platforms
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch
from game.objects.decor.chest import Chest
from game.event import Event
from game.objects.lungs import Lungs
from game.objects.key import Key
from game.objects.extra import Extra
from game.entity import Entity

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player(Entity):
    def __init__(self, x, y):
        #super().__init__()
        self.spritesheet = pygame.image.load(f"../Art/{ConfigManager().get_instance().get_artpath()}/skelly/spritesheet.png") #cargamos las imagenes 
        self.width = self.spritesheet.get_width()/18 # existen 18 imagenes diferentes
        self.height =  self.spritesheet.get_height()
        #self.rect = pygame.Rect(x, y,self.width, self.height) #obtenemos el collisionador
        #self.pos = vec(x, y) #posicion 

        # Llamamos al constructor de Entity con la posición y dimensiones.
        super().__init__(x, y, self.width, self.height)

        self.surf =  self.spritesheet.subsurface(pygame.Rect(0,0, self.width,self.height))
        self.respawn_x = x #coordenada x para reaparecer
        self.respawn_y = y #coordenada y para reaparecer
        self.vel = vec(0, 0) # vector velocidad para los movimientos

        self.ACC =  ConfigManager().get_instance().get_player_Acc()  # constante aceleracion
        self.FRIC =  ConfigManager().get_instance().get_player_fric() # constante friccion (suaviza el movimiento)
        self.speed =  ConfigManager().get_instance().get_player_speed #velocidad de movimiento
        self.jump_Max = ConfigManager().get_instance().get_player_jump() #
        self.y_acc_value =  ConfigManager().get_instance().get_player_Acc()
        self.index = 0 #para cambios en los frames
        self.lifes = 3 # vidas del personaje
       
        #para calculo de tiempo entre acciones
        self.power_up_counter = 0 #para contar cuando el efecto debe desaparecer del power up  (max jump)
        self.death_timer = 0
        self.animation_timer = 0  # mediremos cuanto ha pasado desde el ultimo cambio de imagen para manejar la animación
        self.frame_rate = 10 # limite de cada cuantos frames cambiamos la animación
        
        #Bools para manejo de acciones
        self.power_up = False
        self.jumping = False 
        self.shooting = False
        self.die = False 
        self.direction = 1 # direccion 1 sera derecha y 0 izquierda
        self.frames = {
            "idle": [(0, 0)],  # Una sola imagen para idle
            "walk": [( self.width + (i * self.width), 0) for i in range(4)],  # 4 imágenes para caminar
            "shoot": [(( self.width* 5 ) + ( i * self.width), 0) for i in range(4)],  # 3 imágenes para disparo
            "death": [(( self.width* 15 ) + ( i * self.width), 0) for i in range(3)],   # 3 imágenes para morir  
        }
        self.current_action = "idle"  # Acción inicial
        self.projectiles = Stone() # piedra para lanzar
        self.group = pygame.sprite.Group() #grupo donde se guardaran los elementos para pasar a la clase game y renderizarlos
        self.group.add(self.projectiles)
        self.platform = pygame.sprite.Group() #local para las plataformas y las colisiones, si se revisa en otra clase se eliminará
        #diccionario de acciones
        self.action_map = {
                pygame.K_LEFT: self.handle_walk_left,
                pygame.K_RIGHT: self.handle_walk_right,
                pygame.K_SPACE: lambda: self.handle_jump(self.platform),
                pygame.K_q: self.handle_shoot      
            }
    
    #funciones 
    #para pasar la vida a la clase game
    def get_lifes(self):
        return self.lifes
    
    #funciones relacionadas con las acciones
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

    def handle_shoot(self):
        if self.projectiles.get_inUse():
            self.acc.x = 0
            self.current_action = "idle"
        else:
            self.shooting = True
            self.current_action = "shoot"

    #función que responde a los inputs cambiando la posicion del personaje
    def move(self, platforms):
        if not self.shooting and not self.die: #estas acciones inmovilizan al personaje
            self.acc = vec(0, self.y_acc_value)
            pressed_keys = pygame.key.get_pressed()
            self.platform = platforms
            if not any(pressed_keys):
                self.handle_idle()
                self.pushing = False
            else:
                for key, action in self.action_map.items():
                    if pressed_keys[key] and action:
                        action()

            # Cálculos de posición
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

            # Colocamos la posicion abajo
            self.rect.midbottom = self.pos
            # Actualizamos el rectángulo de colisión según la nueva posición.
            #self.update_rect()
            
        self.action_frames = self.frames[self.current_action]  # Lista de fotogramas para la acción actual
        self.end_index = len(self.action_frames)


    #funcion que nos cambia la imagen a mostrar, la carga y la asigna (ver de convertirlo en diccionario)
    def draw(self):
        if self.current_action == "shoot" and self.index >= self.end_index -1:
            self.shooting = False
            self.shoot()
            self.current_action= "idle"
            self.index = 0
        elif self.current_action == "death" and self.index >= self.end_index -1:
            if self.lifes >= 0 :
                self.index = 0
                self.lifes -=1
                self.die = False
                self.death_timer = 0 
                self.pos.x = self.respawn_x
                self.pos.y = self.respawn_y
                self.rect.topleft = [self.respawn_x , self.respawn_y]
                self.current_action= "idle"   
        elif self.current_action == "idle" or self.index == self.end_index:
            self.index = 0    
        frame = self.action_frames[self.index]
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

    def collision_managment(self, platforms):
        """
        Gestiona las colisiones genéricas llamando al método de la clase padre y
        agrega las colisiones específicas del jugador.
        """
        # Llamamos al método genérico implementado en Entity.
        self.resolve_collisions(platforms, vertical_margin=10)

        # Colisiones específicas de Player:
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:

            # --- COLISIONES CON PINCHOS ---
            if isinstance(hit, Spikes):
                if not self.die and self.death_timer > 100:
                    self.die = True
                    self.pos.y = hit.rect.top + 1
                    self.current_action = "death"
                    self.animation_timer = self.frame_rate + 1

            # --- COLISIONES CON SWITCH ---
            if isinstance(hit, Switch):
                if self.pos.y == hit.rect.topleft[1] + 1:
                    hit.change_position()

            # --- COLISIONES CON CHEST ---
            if isinstance(hit, Chest):
                hit_result = hit.open()
                if hit_result is not None:
                    self.group.add(hit_result)
                # Se resuelve la colisión vertical para el chest, similar a las plataformas
                if self.vel.y > 0 and self.rect.bottom > hit.rect.top and self.rect.top < hit.rect.top:
                    self.rect.bottom = hit.rect.top + 1
                    self.pos.y = self.rect.bottom
                    self.vel.y = 0
                    self.jumping = False
                elif self.vel.y < 0 and self.rect.top < hit.rect.bottom and self.rect.bottom > hit.rect.bottom:
                    self.rect.top = hit.rect.bottom
                    self.pos.y = self.rect.bottom
                    self.vel.y = 0
                self.respawn_x = self.rect.x
                self.respawn_y = self.rect.y

            # --- COLISIONES CON EVENT ---
            if isinstance(hit, Event):
                hit.on_collision(self)

            # --- COLISIONES CON LUNGS (Power-Up de salto) ---
            if isinstance(hit, Lungs):
                if not self.power_up:
                    self.jump_Max = self.jump_Max +(-5)
                    self.power_up_counter = 0
                    self.power_up = True

            # --- COLISIONES CON KEY ---
            if isinstance(hit, Key):
                print("todo key")

            # --- COLISIONES CON EXTRA (vida extra) ---
            if isinstance(hit, Extra):
                self.get_life()


    #Comprobamos si se acaba el powerup (más salto)
    def check_power_up(self):
        if self.power_up_counter >= 3000:
            self.jump_Max = ConfigManager().get_instance().get_player_jump()
            self.power_up= False 
    
    #aumenta el numero de vidas
    def get_life(self):
        if self.lifes < 3:
            self.lifes += 1
                  
    #funcion de actualizacion para ser llamada desde el game loop    
    def update(self, platforms= None):
        self.animation_timer += 1
        self.death_timer += 1
        self.power_up_counter += 1
        if self.power_up:
            self.check_power_up()
        self.move(platforms) # llama a move para gestionar las entradas del teclado
        self.collision_managment(platforms)
        if self.animation_timer > self.frame_rate:
            self.draw()
        #self.projectiles.update(screen) # actualiza los proyectiles en la pantalla se maneja en el game loop de momento
            
