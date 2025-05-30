'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame,  random, utils.globals as globals, utils.auxiliar as auxiliar
from classes.enemy import Enemy


from game.objects.fireball import Fireball
vec = pygame.math.Vector2 #2 for two dimensional



class Boss(Enemy):
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/boss/sprite_sheet.png"))
        super().__init__(x, y, (self.spritesheet.get_width() / 15), self.spritesheet.get_height(), False)
        self.vel = vec(0, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = globals.config.get_player_Acc()   
        self.special_timer = 300
        self.attack = 100
        self.frames = {
            "idle": [(self.width*4, 0)],
            "walk": [(i * self.width, 0) for i in range(2)],
            "melee":  [((self.width * 2 )+(i * self.width), 0) for i in range(2)],
            "magic": [((self.width * 12 )+(i * self.width), 0) for i in range(3)],
            "death": [((self.width * 9 )+(i * self.width), 0) for i in range(2)],
            "dash": [((self.width * 11 )+(i * self.width), 0) for i in range(1)]

        }
        self.animation_map.update({
            "melee" : self.other_animation,
            "magic": self.other_animation,
            "death": self.other_animation,
            "dash": self.other_animation      
         })
        self.animation_map["death"] = self.the_end
        self.hurt_sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("hurt.wav")))
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("win.wav")))
        self.sound.set_volume(0.5)
        self.lifes = 50
        for i in range(5):
            self.group.add(Fireball())
        self.dash_speed = 5
        self.dash_duration = 30
        self.dash_timer = 0
        
    #region move
    def move(self):
        """
        Mueve al jefe por la pantalla y gestiona sus acciones.

        :return: None
        """
        if self.current_action != "death":
            self.set_objective()
            distance_x = self.objective[0] - self.rect.x
            if distance_x < 0:
                self.direction = -1
            else:
                self.direction = 1
            # Si el jefe está en estado especial, no se mueve hasta que pase el tiempo
            if  self.current_action == "magic":
                self.special_timer -= 1
                if self.special_timer <= 0:
                    self.current_action = "walk" 
                    self.index = 0
                if self.special_timer % 6 ==0:
                    self.magic_attack() 
                
            elif abs(distance_x) < self.screen_width/3 and self.lifes < 25 and self.attack <= 0:
                self.current_action = "magic"
                self.index = 0
                self.magic_attack()
                self.attack = 600
                self.special_timer = 300
            elif self.dash_timer > 0  and self.lifes < 30 and self.attack <= 0:
                self.dash_timer -= 1
                self.vel.x = self.dash_speed * self.direction
                self.pos.x += self.vel.x
                self.update_rect()
                if self.dash_timer == 0:
                    self.current_action = "walk"
            else:
                self.vel.x = self.speed * self.direction
                self.pos.x += self.vel.x
                self.update_rect()
                if abs(distance_x) < int(self.screen_width/12):
                    if self.current_action != "melee":
                        self.index = 0
                    self.current_action = "melee"
                else:
                    if self.current_action != "walk":
                        self.index = 0  
                    self.current_action = "walk"
    #endregion

    #region the_end
    def the_end(self):
        """
        Gestiona la animación final del jefe y la transición a la siguiente escena.

        :return: None
        """
        if self.index == self.end_index:
            self.index -= 1
            self.sound.play()
            globals.game.scene.running= False
            globals.game.load_start("st5.json")
    #endregion
                                
    #region magic_attack
    def magic_attack(self):
        """
        Realiza el ataque mágico del jefe, activando un Fireball.

        :return: None
        """
        for item in self.group:
            if not item.get_inUse():
                random_x = random.randint(self.rect.x - 300, self.rect.x + 300)
                item.active(random_x, self.height*3, 1)
                break
    #endregion
            
    #region update
    def update(self):
        """
        Actualiza el estado del jefe, incluyendo el temporizador de ataque, el temporizador de animación y el movimiento.
        También incluye la posibilidad de que el boss haga 'dash' de manera aleatoria.
        :return: None
        """
        self.attack -= 1
        self.animation_timer += 1
        self.move()
        if self.current_action == "walk" and random.randint(0, 100) < 5:
            self.dash()
    #endregion
 
    #region draw
    def draw(self, screen= None, position = None):
        """
        Dibuja el jefe.

        :param screen: Superficie sobre la que dibujar.
        :param position: Posición en la que colocar el jefe.
        :return: None
        """
        self.render()
        screen.blit(self.surf,position)
    #endregion   
        
    #region die
    def die(self):
        """
        Gestiona la muerte del jefe, reproduciendo un sonido y cambiando su estado.

        :return: None
        """
        if not self.hit:
            self.hurt_sound.play()
            self.hit = True
            self.wounded()
    #endregion
                                       
    #region wounded
    def wounded(self):
        """
        Reduce las vidas del jefe y gestiona la transición a la animación de muerte si las vidas llegan a 0.

        :return: None
        """
        self.lifes -= 1
        if self.lifes == 0:
            self.current_action = "death"
            self.index = 0
        else:
            self.hit = False
    #endregion
            
    #region dash
    def dash(self):
        """
        Inicia el movimiento de embestida (dash) del jefe.

        :return: None
        """
        if self.dash_timer == 0:
            self.current_action = "dash"
            self.index = 0
            self.dash_timer = self.dash_duration
    #endregion