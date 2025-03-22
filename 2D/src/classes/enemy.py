'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.globals as globals, utils.auxiliar as auxiliar

from classes.entity import Entity
from game.objects.stone import Stone
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad

class Enemy(Entity):
    """
    Clase base para los enemigos que hereda de Entity.
    Incorpora movimiento y una resolución de colisiones adaptada:
      - Si colisiona lateralmente con una plataforma, cambia de dirección (rebota).
      - Si cae sobre una plataforma, se asienta sobre ella.
      - Si colisiona con un jugador, se comporta igual que con los spikes.
    """
    def __init__(self, x, y, width, height,  path = True):
        # Cargamos el sprite sheet del enemigo (por ejemplo, un murciélago).
        if path:
           self.spritesheet = pygame.Surface((60, 60))
           self.spritesheet.fill((0, 0, 0))
        # Llamamos al constructor de Entity para establecer posición y el rectángulo de colisión.
        super().__init__(x, y, width, height)
        # Asignamos la imagen completa como superficie inicial.
        self.surf = self.spritesheet.subsurface(pygame.Rect(0,0,self.width, self.height))
        # Configuración de velocidad y movimiento
        self.change_direction_interval = 60  # Opcional: intervalos para cambiar dirección.
        self.frame_counter = 0 
        # Dimensiones de la pantalla (para rebotar en los bordes).
        self.screen_width =  globals.config.get_width()
        self.screen_height =  globals.config.get_height()
        # Variables para animación.
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(0, 0)],
            "death": [(0, 0)]
        }
        self.current_action = "walk"
        #otras variables
        self.on_screen = False
        self.hit = False
        self.not_death = True
        self.respawn_time = 3600
        self.lifes = 1
        self.sound = pygame.mixer.Sound(auxiliar.get_path(f"{globals.config.get_audiofxpath("hit.wav")}"))
        self.sound.set_volume(0.5)
        
        self.animation_map.update({
            "death": self.other_animation         
         })
        

    """
        Actualiza la posición del enemigo en función de su velocidad y rebota en los bordes.
    """
    #funcion que gestiona el movimiento
    def move(self):
        
        self.pos.x += self.vel.x * self.speed
        self.pos.y += self.vel.y * self.speed

        # Rebote en los bordes horizontales.
        if self.pos.x > self.screen_width - self.rect.width:
            self.vel.x = -abs(self.vel.x)
        if self.pos.x < 0:
            self.vel.x = abs(self.vel.x)
        # Rebote en los bordes verticales.
        if self.pos.y > self.screen_height - self.rect.height:
            self.vel.y = -abs(self.vel.y)
        if self.pos.y < 0:
            self.vel.y = abs(self.vel.y)
        
        # Actualizamos el rectángulo de colisión.
        self.update_rect()

    #funcion que maneja las colisiones de los enemigos
    """
        Gestiona las colisiones genéricas utilizando el método de la clase padre
        y añade la condición para colisión con un jugador (Player), comportándose igual que con spikes.
    """
    def collision_managment(self, platforms):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # Colisiones específicas: si choca con un jugador, invertimos la velocidad (comportamiento similar a spikes).
        for hit in hits:
            self.resolve_collisions(hit, vertical_margin=10)
            if isinstance(hit, Stone):
                hit.hit()
                # Al colisionar con un jugador, invertimos la velocidad.
                if not self.hit:    
                    self.die()       
                        
    #Funcion que actualiza la posicion del jugador si es necesario            
    def update(self):
        if self.on_screen :
            if self.not_death:
                self.animation_timer += 1
                self.move()
                if self.vel.x != 0:
                    self.current_action = "walk"
                else:
                    self.current_action = "idle"       
            else:
                self.respawn_time -=1
                self.check_respawn()
        else:     
            if not self.not_death:
                self.respawn_time -= 1
                self.check_respawn()
        
    def check_respawn(self):
        if self.respawn_time <=0:
            self.respawn_time = 3000
            self.not_death = True
            self.lifes = 1
            self.hit =False
            self.rect = self.surf.get_rect(topleft=(self.respawn_x, self.respawn_y))
 
    #Funcion de dibujado en pantalla
    def draw(self, screen= None, position = None):
        if self.on_screen and self.not_death:
            self.render()
            screen.blit(self.surf,position)  
        
    #Gestionamos la colision y muerte
    def die(self):
        if not self.hit:
            self.vel = -self.vel
            self.current_action = "death"
            self.hit = True
            self.wounded()
    
    def wounded(self):
        self.lifes -= 1
        self.sound.play()
        if self.lifes<= 0:
            self.not_death = False
            self.rect.topleft = (-100, -100)
        else:
            self.hit = False

    #Funcion que establece un objetivo para el enemigo    
    def set_objective(self):
        aux = globals.game.player_position()
        if aux == None:
            return
        else:
            self.objective = aux