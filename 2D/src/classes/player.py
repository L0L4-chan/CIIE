'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame,  utils.globals as globals, utils.auxiliar as auxiliar
from game.objects.stone import Stone
from game.objects.fireball import Fireball
from game.objects.decor.spikes import Spikes
from game.objects.decor.switch import Switch
from game.objects.decor.chest import Chest
from game.objects.decor.event import Event
from game.objects.lungs import Lungs
from game.objects.key import Key
from game.objects.extra import Extra
from classes.entity import Entity

vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Player(Entity):
    def __init__(self, x, y):
        # Cargamos el sprite sheet y definimos ancho y alto.
        self.spritesheet = pygame.image.load(auxiliar.get_path(
            f"{ globals.config.get_artpath()}/skelly/spritesheet.png"
        ))
        self.width = self.spritesheet.get_width() / 18  # 18 imágenes diferentes.
        self.height = self.spritesheet.get_height()
        # Llamamos al constructor de Entity con posición y dimensiones.
        super().__init__(x, y, self.width, self.height)
        self.surf = self.spritesheet.subsurface(pygame.Rect(0, 0, self.width, self.height))
        self.vel = vec(0, 0)
        self.got_key = False
        self.ACC =  globals.config.get_player_Acc()
        self.FRIC =  globals.config.get_player_fric()
        self.speed =  globals.config.get_player_speed()
        self.jump_Max =  globals.config.get_player_jump()
        self.y_acc_value =  globals.config.get_player_Acc()
        self.lifes = 3
        self.death_sound = pygame.mixer.Sound(auxiliar.get_path(f"{globals.config.get_audiofxpath()}death.wav"))
        self.power_up_sound = pygame.mixer.Sound(auxiliar.get_path(f"{globals.config.get_audiofxpath()}ticktock.wav"))
        self.power_up_counter = 0
        self.death_timer = 0
        self.power_up = False
        self.jumping = False 
        self.shooting = False
        self.die = False 
        self.got_life = False
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(self.width + (i * self.width), 0) for i in range(4)],
            "shoot": [((self.width * 5) + (i * self.width), 0) for i in range(4)],
            "death": [((self.width * 15) + (i * self.width), 0) for i in range(3)],
        }      
        self.current_action = "idle"
        self.projectiles = Stone()
        self.group.add(self.projectiles)
        # Grupo local para las plataformas (se usa para pasar las colisiones, normalmente se llena en Game)
        self.platform = pygame.sprite.Group()
        # Diccionario de acciones para las entradas.
        self.action_map = {
            pygame.K_LEFT: self.handle_walk_left,
            pygame.K_RIGHT: self.handle_walk_right,
            pygame.K_SPACE: self.handle_jump,
            pygame.K_q: self.handle_shoot
        }
        #diccionario para animaciones 
        self.animation_map.update({
            "shoot":self.end_shooting,
            "death": self.animation_death          
         })
        
    def get_lifes(self):
        return self.lifes

    def handle_idle(self):
        self.acc.x = 0
        self.current_action = "idle"

    def handle_walk_left(self):
        self.acc.x = -self.ACC
        self.direction = -1
        self.current_action = "walk"

    def handle_walk_right(self):
        self.acc.x = self.ACC
        self.direction = 1
        self.current_action = "walk"

    def handle_jump(self):
        hits = pygame.sprite.spritecollide(self, self.platform, False)
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

    def move(self):
        if not self.shooting and not self.die:
            self.acc = vec(0, self.y_acc_value)
            pressed_keys = pygame.key.get_pressed()

            if not any(pressed_keys):
                self.handle_idle()
                self.pushing = False
            else:
                for key, action in self.action_map.items():
                    if pressed_keys[key] and action:
                        action()
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + self.ACC * self.acc
            self.update_rect()
       
    def end_shooting(self):
        if self.index >= self.end_index:
            self.shoot()
            self.shooting = False
            self.current_action = "idle"
            self.index = 0

    def end_of_death(self): 
        self.death_sound.play()
        self.index = 0
        self.lifes -= 1
        self.die = False
        self.power_up = False
        self.power_up_sound.stop()
        self.jump_Max =  globals.config.get_player_jump()
        self.jumping = False 
        self.shooting = False
        self.death_timer = 0
        self.pos.x = self.respawn_x
        self.pos.y = self.respawn_y
        self.rect.topleft = [self.respawn_x, self.respawn_y]
        self.current_action = "idle"
    
    def animation_death(self):
        if self.index >= self.end_index:
                if self.lifes >= 0:
                    self.end_of_death()
                else:
                    self.index -=1   
    
         
    
    

    #funcion de dibujado en pantalla
    def draw(self, screen, position = None):
        if self.animation_timer > self.frame_rate:
            self.render()
        screen.blit(self.surf,position)  

    #funcion de gestion de disparo
    def shoot(self):
        if self.direction > 0:
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        self.projectiles.active(x=stone_x, y=stone_y, direction=self.direction)

    #definicion de colisones
    def collision_managment(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # Colisiones específicas: si choca con un jugador, invertimos la velocidad (comportamiento similar a spikes).
        for hit in hits:
            self.resolve_collisions(hit, vertical_margin=10)
            # --- COLISIONES CON PINCHOS ---
            if isinstance(hit, Spikes):
                if not self.die and self.death_timer > 100:
                    self.pos.y = hit.rect.top + 1
                    self.to_die()
            
            # --- COLISIONES CON ENEMY ---
            from classes.enemy import Enemy  # Importación local
            if isinstance(hit, Enemy):
                if not self.die and self.death_timer > 100:
                    self.to_die()
                from enemies.boss import Boss
                if not isinstance(hit, Boss):
                    hit.die()
                
            # --- COLISIONES CON STONE O FIREBALL---
            if isinstance(hit, Stone) or isinstance(hit, Fireball):
                if not self.die and self.death_timer > 100:
                    self.to_die()
                hit.hit()
              
            # --- COLISIONES CON SWITCH ---
            if isinstance(hit, Switch):
                if self.pos.y == hit.rect.topleft[1] + 1:
                    hit.change_position()
            
            # --- COLISIONES CON CHEST ---
            if isinstance(hit, Chest):
                hit_result = hit.open()
                self.respawn_x = self.rect.x
                self.respawn_y = self.rect.y
            
            # --- COLISIONES CON EVENT ---
            if isinstance(hit, Event):
                if self.got_key:
                    hit.on_collision(self)
                else:
                    hit.sound.play()
                    hit.no_key(self.lifes-1)

            # --- COLISIONES CON LUNGS (Power-Up de salto) ---
            if isinstance(hit, Lungs):
                if not self.power_up:
                    hit.sound.play()
                    self.jump_Max += self.jump_Max  * self.ACC
                    self.power_up_counter = 0
                    self.power_up_sound.play()
                    self.power_up = True
            
            # --- COLISIONES CON KEY ---
            if isinstance(hit, Key):
                if not self.got_key:
                    hit.sound.play()
                    self.got_key = True
                    hit.kill()
            
            # --- COLISIONES CON EXTRA (vida extra) ---
            if isinstance(hit, Extra):
                    self.get_life(hit)

    def check_power_up(self):
        if self.power_up_counter >= 1690:
            self.jump_Max =  globals.config.get_player_jump()
            self.power_up = False

    #aumenta el numero de vidas
    def get_life(self, hit):
        if hit.get_can_pick():
            if self.lifes < 3:
                self.lifes += 1
                hit.sound.play()
            hit.being_pick()

    def to_die(self):
        self.die = True
        self.current_action = "death"
        self.index = 0
        self.animation_timer = self.frame_rate + 1
    
    def update(self):
        self.animation_timer += 1
        self.death_timer += 1
        self.power_up_counter += 1
        if self.power_up:
            self.check_power_up()
        self.move()
              
    def get_group(self):
        return self.group
        
    def set_platform(self, platform):
        self.platform = platform
       