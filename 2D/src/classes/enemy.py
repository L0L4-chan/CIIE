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
    def __init__(self, x, y, width, height, path = True):
        # Cargamos el sprite sheet del enemigo (por ejemplo, un murciélago).
        if path:
           self.spritesheet = pygame.Surface((60, 60))
           self.spritesheet.fill((0, 0, 0))
        # Llamamos al constructor de Entity para establecer posición y el rectángulo de colisión.
        super().__init__(x, y, width, height)
        # Asignamos la imagen completa como superficie inicial.
        self.surf = self.spritesheet.subsurface(pygame.Rect(0,0,self.width, self.height))
        # Configuración de velocidad y movimiento.
        self.vel = vec(1, 1)      # Velocidad inicial genérica.
        self.speed = 2            # Factor de velocidad.
        self.change_direction_interval = 60  # Opcional: intervalos para cambiar dirección.
        self.frame_counter = 0 
        # Dimensiones de la pantalla (para rebotar en los bordes).
        self.screen_width = ConfigManager().get_instance().get_width()
        self.screen_height = ConfigManager().get_instance().get_height()
        # Variables para animación.
        self.animation_timer = 0
        self.frame_rate = 10
        self.index = 0
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(0, 0)],
            "death": [(0, 0)]
        }
        self.current_action = "walk"
        #otras variables
        self.group = pygame.sprite.Group()
        self.on_screen = False
        self.hit = False
        self.lifes = 1

    #funcion que gestiona el movimiento
    def move(self):
        """
        Actualiza la posición del enemigo en función de su velocidad y rebota en los bordes.
        """
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
    def collision_managment(self, platforms):
        """
        Gestiona las colisiones genéricas utilizando el método de la clase padre
        y añade la condición para colisión con un jugador (Player), comportándose igual que con spikes.
        """
        # Creamos un grupo unificado: combinamos plataformas y enemigos.
        collidables = platforms.copy()  # Copiamos el grupo de plataformas.
        # Llamamos al método genérico de colisiones de Entity.
        self.resolve_collisions(collidables, vertical_margin=10)
        # Luego, comprobamos colisiones específicas:
        hits = pygame.sprite.spritecollide(self, collidables, False)
        # Colisiones específicas: si choca con un jugador, invertimos la velocidad (comportamiento similar a spikes).
        for hit in hits:
            print(hit)
            if isinstance(hit, Stone):
                print("Enemy Colisión con Stone detectada")
                # Al colisionar con un jugador, invertimos la velocidad.
                hit.set_use()
                self.die()
        
    #funcion que actualiza la posicion del jugador si es necesario            
    def update(self):
        if self.on_screen:
            self.animation_timer += 1
            self.move()
            if self.vel.x != 0:
                self.current_action = "walk"
            else:
                self.current_action = "idle"       
    
    def render(self):
        action_frames = self.frames[self.current_action]
        if self.animation_timer > self.frame_rate:
            self.index += 1
            if self.index >= len(action_frames)-1:
                self.index = 0
            self.animation_timer = 0
            frame = action_frames[self.index]
            sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], self.width, self.height))
            if self.vel.x < 0:
                sprite_image = pygame.transform.flip(sprite_image, True, False)
            self.surf = sprite_image
    
    #funcion de dibujado en pantalla
    def draw(self, screen= None, position = None):
        if self.on_screen:
            self.render()
            screen.blit(self.surf,position)  
        
    #gestionamos la colision y muerte
    def die(self):
        print("Enemy Colisión con Player detectada")
        
        if not self.hit:
            # Al colisionar con un jugador, invertimos la velocidad.
            self.vel = -self.vel
            self.current_action = "death"
            self.hit = True
            self.wounded()
    
    def wounded(self):
        self.lifes -= 1
        if self.lifes<= 0:
            self.kill()
    
    #funcion que establece un objetivo para el enemigo    
    def set_objective(self, position_player=None):
        self.objective = position_player