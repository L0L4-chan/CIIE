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
        #variables de movimiento que dependen de la configuracion de tamaño de la pantalla
        self.ACC =  globals.config.get_player_Acc()
        self.FRIC =  globals.config.get_player_fric()
        self.speed =  globals.config.get_player_speed()
        self.jump_Max =  globals.config.get_player_jump()
        self.y_acc_value =  globals.config.get_player_Acc()
        # Otras variables de estado.
        self.lifes = 3
        self.death_sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("death.wav")))
        self.power_up_sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("ticktock.wav")))
        self.power_up_counter = 0
        self.death_timer = 0
        self.got_key = False
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
        
    #region get_lifes
    def get_lifes(self):
        """
        Obtiene el número de vidas del jugador.
        :return: Número de vidas.
        """
        return self.lifes
    #endregion

    #region handle_idle
    def handle_idle(self):
        """
        Maneja el estado idle (parado) del jugador.
        """
        self.acc.x = 0
        self.current_action = "idle"
    #endregion

    #region handle_walk_left
    def handle_walk_left(self):
        """
        Maneja el movimiento hacia la izquierda.
        """
        self.acc.x = -self.ACC
        self.direction = -1
        self.current_action = "walk"
    #endregion

    #region handle_walk_right
    def handle_walk_right(self):
        """
        Maneja el movimiento hacia la derecha.
        """
        self.acc.x = self.ACC
        self.direction = 1
        self.current_action = "walk"
    #endregion

    #region handle_jump
    def handle_jump(self):
        """
        Maneja el salto del jugador.
        """
        hits = pygame.sprite.spritecollide(self, self.platform, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = self.jump_Max
    #endregion

    #region handle_shoot
    def handle_shoot(self):
        """
        Maneja la acción de disparar.
        """
        if self.projectiles.get_inUse():
            self.acc.x = 0
            self.current_action = "idle"
        else:
            self.shooting = True
            self.current_action = "shoot"
    #endregion

    #region move
    def move(self):
        """
        Controla el movimiento general del jugador.
        """
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
    #endregion

    #region end_shooting
    def end_shooting(self):
        """
        Finaliza la animación de disparo.
        """
        if self.index >= self.end_index:
            self.shoot()
            self.shooting = False
            self.current_action = "idle"
            self.index = 0
    #endregion

    #region end_of_death
    def end_of_death(self): 
        """
        Resetea parámetros tras la muerte del jugador.
        """
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
    #endregion

    #region animation_death
    def animation_death(self):
        """
        Maneja la animación de muerte.
        """
        if self.index >= self.end_index:
                if self.lifes >= 0:
                    self.end_of_death()
                else:
                    self.index -=1   
    #endregion

    #region draw
    def draw(self, screen, position = None):
        """
        Dibuja el jugador en pantalla.
        :param screen: Superficie donde dibujar.
        :param position: Posición del jugador.
        """
        if self.animation_timer > self.frame_rate:
            self.render()
        screen.blit(self.surf,position)  
    #endregion

    #region shoot
    def shoot(self):
        """
        Ejecuta la acción de disparo.
        """
        if self.direction > 0:
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        self.projectiles.active(x=stone_x, y=stone_y, direction=self.direction)
    #endregion

    #region collision_managment
    def collision_managment(self, platforms):
        """
        Gestiona todas las colisiones del jugador.
        :param platforms: Plataformas y objetos a comprobar.
        """
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            self.resolve_collisions(hit, vertical_margin=10)
            from classes.enemy import Enemy  # Importación local
            if isinstance(hit, Spikes):
                if not self.die and self.death_timer > 100:
                    self.pos.y = hit.rect.top + 1
                    self.to_die()
            if isinstance(hit, Enemy):
                if not self.die and self.death_timer > 100:
                    self.to_die()
                from enemies.boss import Boss
                if not isinstance(hit, Boss):
                    hit.die()
            if isinstance(hit, Stone) or isinstance(hit, Fireball):
                if not self.die and self.death_timer > 100:
                    self.to_die()
                hit.hit()
            if isinstance(hit, Switch):
                if self.pos.y == hit.rect.topleft[1] + 1:
                    hit.change_position()
            if isinstance(hit, Chest):
                hit_result = hit.open()
                self.respawn_x = self.rect.x
                self.respawn_y = self.rect.y
            if isinstance(hit, Event):
                if self.got_key:
                    hit.on_collision(self)
                else:
                    hit.sound.play()
                    hit.no_key(self.lifes-1)
            if isinstance(hit, Lungs):
                if not self.power_up:
                    hit.sound.play()
                    self.jump_Max += self.jump_Max  * self.ACC
                    self.power_up_counter = 0
                    self.power_up_sound.play()
                    self.power_up = True
            if isinstance(hit, Key):
                if not self.got_key:
                    hit.sound.play()
                    self.got_key = True
                    hit.kill()
            if isinstance(hit, Extra):
                    self.get_life(hit)
    #endregion

    #region check_power_up
    def check_power_up(self):
        """
        Verifica si el power-up ha expirado.
        """
        if self.power_up_counter >= 1690:
            self.jump_Max =  globals.config.get_player_jump()
            self.power_up = False
    #endregion

    #region get_life
    def get_life(self, hit):
        """
        Incrementa vidas si es posible.
        :param hit: Objeto de tipo Extra.
        """
        if hit.get_can_pick():
            if self.lifes < 3:
                self.lifes += 1
                hit.sound.play()
            hit.being_pick()
    #endregion

    #region to_die
    def to_die(self):
        """
        Maneja la muerte del jugador.
        """
        self.die = True
        self.current_action = "death"
        self.index = 0
        self.animation_timer = self.frame_rate + 1
    #endregion

    #region update
    def update(self):
        """
        Actualiza el estado del jugador.
        """
        self.animation_timer += 1
        self.death_timer += 1
        self.power_up_counter += 1
        if self.power_up:
            self.check_power_up()
        self.move()
    #endregion

    #region get_group
    def get_group(self):
        """
        Devuelve el grupo de proyectiles.
        :return: Grupo.
        """
        return self.group
    #endregion

    #region set_platform
    def set_platform(self, platform):
        """
        Asigna las plataformas del nivel.
        :param platform: Grupo de plataformas.
        """
        self.platform = platform
    #endregion