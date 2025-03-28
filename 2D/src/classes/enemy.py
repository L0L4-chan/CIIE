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
    
    #region __init__
    def __init__(self, x, y, width, height, path=True):
        """
        Constructor de la clase Enemy, inicializa el enemigo con sus atributos.

        :param x: Posición X del enemigo.
        :param y: Posición Y del enemigo.
        :param width: Ancho del rectángulo de colisión del enemigo.
        :param height: Alto del rectángulo de colisión del enemigo.
        :param path: Parámetro que indica si se carga el sprite del enemigo.
        """
        # Cargamos el sprite sheet del enemigo (por ejemplo, un murciélago).
        if path:
           self.spritesheet = pygame.Surface((60, 60))
           self.spritesheet.fill((0, 0, 0))
        # Llamamos al constructor de Entity para establecer posición y el rectángulo de colisión.
        super().__init__(x, y, width, height)
        # Asignamos la imagen completa como superficie inicial.
        self.surf = self.spritesheet.subsurface(pygame.Rect(0, 0, self.width, self.height))
        # Configuración de velocidad y movimiento
        self.change_direction_interval = 60  # Opcional: intervalos para cambiar dirección.
        self.frame_counter = 0 
        # Dimensiones de la pantalla (para rebotar en los bordes).
        self.screen_width = globals.config.get_width()
        self.screen_height = globals.config.get_height()
        # Variables para animación.
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(0, 0)],
            "death": [(0, 0)]
        }
        self.current_action = "walk"
        # otras variables
        self.on_screen = False #evitara el renderizado de los enemigos que no esten en pantalla
        self.hit = False 
        self.not_death = True
        self.respawn_time = 3600 #tiempo de respawn
        self.lifes = 1
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("hit.wav")))
        self.sound.set_volume(0.5)
        
        self.animation_map.update({
            "death": self.other_animation         
        })
    #endregion
    
    #region move
    def move(self):
        """
        Actualiza la posición del enemigo en función de su velocidad y rebota en los bordes.

        :param None:
        :return: None
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
    #endregion

    #region collision_managment
    def collision_managment(self, platforms):
        """
        Gestiona las colisiones genéricas utilizando el método de la clase padre
        y añade la condición para colisión con un jugador (Player), comportándose igual que con spikes.

        :param platforms: Lista de plataformas con las que el enemigo puede colisionar.
        :return: None
        """
        hits = pygame.sprite.spritecollide(self, platforms, False)
        # Colisiones específicas: si choca con un jugador, invertimos la velocidad (comportamiento similar a spikes).
        for hit in hits:
            self.resolve_collisions(hit, vertical_margin=10)
            if isinstance(hit, Stone):
                hit.hit()
                # Al colisionar con un jugador, invertimos la velocidad.
                if not self.hit:    
                    self.die()
    #endregion

    #region update
    def update(self):
        """
        Actualiza el estado del enemigo, gestionando su movimiento, animación y tiempos de respawn.

        :return: None
        """
        if self.on_screen:
            if self.not_death:
                self.animation_timer += 1
                self.move()
                if self.vel.x != 0:
                    self.current_action = "walk"
                else:
                    self.current_action = "idle"
            else:
                self.respawn_time -= 1
                self.check_respawn()
        else:
            if not self.not_death:
                self.respawn_time -= 1
                self.check_respawn()
    #endregion

    #region check_respawn
    def check_respawn(self):
        """
        Verifica si el enemigo debe reaparecer tras haber muerto.

        :return: None
        """
        if self.respawn_time <= 0:
            self.respawn_time = 3000
            self.not_death = True
            self.lifes = 1
            self.hit = False
            self.rect = self.surf.get_rect(topleft=(self.respawn_x, self.respawn_y))
    #endregion

    #region draw
    def draw(self, screen=None, position=None):
        """
        Dibuja el enemigo en la pantalla.

        :param screen: Superficie sobre la que dibujar.
        :param position: Posición en la que colocar el enemigo.
        :return: None
        """
        if self.on_screen and self.not_death:
            self.render()
            screen.blit(self.surf, position)
    #endregion

    #region die
    def die(self):
        """
        Gestiona la muerte del enemigo, invirtiendo su velocidad y cambiando su animación.

        :return: None
        """
        if not self.hit:
            self.vel = -self.vel
            self.current_action = "death"
            self.hit = True
            self.wounded()
    #endregion

    #region wounded
    def wounded(self):
        """
        Maneja el daño recibido por el enemigo, reduciendo sus vidas y reproduciendo un sonido de impacto.

        :return: None
        """
        self.lifes -= 1
        self.sound.play()
        if self.lifes <= 0:
            self.not_death = False
            self.rect.topleft = (-100, -100)
        else:
            self.hit = False
    #endregion

    #region set_objective
    def set_objective(self):
        """
        Establece un objetivo para el enemigo, como la posición del jugador.

        :return: None
        """
        aux = globals.game.player_position()
        if aux is None:
            return
        else:
            self.objective = aux
    #endregion
