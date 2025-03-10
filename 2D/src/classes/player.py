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
        # Cargamos el sprite sheet y definimos ancho y alto.
        self.spritesheet = pygame.image.load(
            f"../Art/{ConfigManager().get_instance().get_artpath()}/skelly/spritesheet.png"
        )
        self.width = self.spritesheet.get_width() / 18  # 18 imágenes diferentes.
        self.height = self.spritesheet.get_height()
        # Llamamos al constructor de Entity con posición y dimensiones.
        super().__init__(x, y, self.width, self.height)
        self.surf = self.spritesheet.subsurface(pygame.Rect(0, 0, self.width, self.height))
        self.respawn_x = x
        self.respawn_y = y
        self.vel = vec(0, 0)
        
        self.got_key = False
        self.ACC = ConfigManager().get_instance().get_player_Acc()
        self.FRIC = ConfigManager().get_instance().get_player_fric()
        self.speed = ConfigManager().get_instance().get_player_speed()
        self.jump_Max = ConfigManager().get_instance().get_player_jump()
        self.y_acc_value = ConfigManager().get_instance().get_player_Acc()
        self.index = 0
        self.lifes = 3
        self.death_sound = pygame.mixer.Sound("../Sound/FX/death.wav")
        self.power_up_sound = pygame.mixer.Sound("../Sound/FX/ticktock.wav")
        self.power_up_counter = 0
        self.death_timer = 0
        self.animation_timer = 0
        self.frame_rate = 10
        self.power_up = False
        self.jumping = False 
        self.shooting = False
        self.die = False 
        self.got_life = False
        self.direction = 1  # 1: derecha, 0: izquierda
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(self.width + (i * self.width), 0) for i in range(4)],
            "shoot": [((self.width * 5) + (i * self.width), 0) for i in range(4)],
            "death": [((self.width * 15) + (i * self.width), 0) for i in range(3)],
        }
        self.current_action = "idle"
        self.projectiles = Stone()
        self.group = pygame.sprite.Group()
        self.group.add(self.projectiles)
        # Grupo local para las plataformas (se usa para pasar las colisiones, normalmente se llena en Game)
        self.platform = pygame.sprite.Group()
        # <--- Aquí definimos el grupo de enemigos que se usará en las colisiones.
        self.enemy_group = pygame.sprite.Group()  # Inicialmente vacío; desde Game o en otro módulo lo llenas.
        # Diccionario de acciones para las entradas.
        self.action_map = {
            pygame.K_LEFT: self.handle_walk_left,
            pygame.K_RIGHT: self.handle_walk_right,
            pygame.K_SPACE: lambda: self.handle_jump(self.platform),
            pygame.K_q: self.handle_shoot
        }

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

    def handle_shoot(self):
        if self.projectiles.get_inUse():
            self.acc.x = 0
            self.current_action = "idle"
        else:
            self.shooting = True
            self.current_action = "shoot"

    def move(self, platforms):
        if not self.shooting and not self.die:
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
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            self.rect.midbottom = self.pos
            self.update_rect()
        self.action_frames = self.frames[self.current_action]
        self.end_index = len(self.action_frames)

    def draw(self):
        if self.current_action == "shoot" and self.index >= self.end_index - 1:
            self.shooting = False
            self.shoot()
            self.current_action = "idle"
            self.index = 0
        elif self.current_action == "death" and self.index >= self.end_index - 1:
            if self.lifes >= 0:
                self.death_sound.play()
                self.index = 0
                self.lifes -= 1
                self.die = False
                self.death_timer = 0
                self.pos.x = self.respawn_x
                self.pos.y = self.respawn_y
                self.rect.topleft = [self.respawn_x, self.respawn_y]
                self.current_action = "idle"
        elif self.current_action == "idle" or self.index == self.end_index:
            self.index = 0
        frame = self.action_frames[self.index]
        sprite_image = self.spritesheet.subsurface(pygame.Rect(frame[0], frame[1], self.width, self.height))
        if self.direction == 0:
            sprite_image = pygame.transform.flip(sprite_image, True, False)
        self.surf = sprite_image
        self.animation_timer = 0
        self.index += 1

    def shoot(self):
        if self.direction:
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        self.projectiles.active(x=stone_x, y=stone_y, direction=self.direction)


    def collision_managment(self, platforms):
        # Creamos un grupo unificado: combinamos plataformas y enemigos.
        collidables = platforms.copy()  # Copiamos el grupo de plataformas.
        if self.enemy_group and len(self.enemy_group) > 0:
            # Añadimos todos los enemigos.
            collidables.add(*self.enemy_group.sprites())
        # Llamamos al método genérico de colisiones de Entity.
        self.resolve_collisions(collidables, vertical_margin=10)
        # Luego, comprobamos colisiones específicas:
        hits = pygame.sprite.spritecollide(self, collidables, False)
        for hit in hits:

            # --- COLISIONES CON PINCHOS ---
            if isinstance(hit, Spikes):
                if not self.die and self.death_timer > 100:
                    print("Colisión con Spikes detectada")
                    self.die = True
                    self.pos.y = hit.rect.top + 1
                    self.current_action = "death"
                    self.animation_timer = self.frame_rate + 1
                    for sprite in collidables:
                        print(type(sprite).__name__, sprite.rect)
            
            # --- COLISIONES CON ENEMY ---
            from classes.enemy import Enemy  # Importación local
            if isinstance(hit, Enemy):
                if not self.die and self.death_timer > 100:
                    print("Colisión con Enemy detectada")
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
                if self.got_key:
                    hit.on_collision(self)
                else:
                    hit.sound.play()
                    hit.no_key(self.lifes-1)

            # --- COLISIONES CON LUNGS (Power-Up de salto) ---
            if isinstance(hit, Lungs):
                if not self.power_up:
                    hit.sound.play()
                    self.jump_Max = self.jump_Max + (-5)
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
        if self.power_up_counter >= 2000:
            self.jump_Max = ConfigManager().get_instance().get_player_jump()
            self.power_up = False

    #aumenta el numero de vidas
    def get_life(self, hit):
        if hit.get_can_pick():
            if self.lifes < 3:
                self.lifes += 1
                hit.sound.play()
            hit.being_pick()

    def update(self, platforms=None):
        self.animation_timer += 1
        self.death_timer += 1
        self.power_up_counter += 1
        if self.power_up:
            self.check_power_up()
        self.move(platforms)
        self.collision_managment(platforms)
        if self.animation_timer > self.frame_rate:
            self.draw()
