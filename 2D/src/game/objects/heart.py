'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame, utils.auxiliar as auxiliar, utils.globals as globals
from game.objects.decor.breakable import Breakable
from game.objects.decor.platforms import Platforms
from game.objects.oneuse import OneUse
vec = pygame.math.Vector2  # Vector para cálculos de posición y velocidad
class Heart(OneUse):
    #region __init__
    def __init__(self):
        """
        Inicializa la clase Heart.

        Carga la spritesheet, define dimensiones, frames de animación, sonido y atributos iniciales.
        """
        super().__init__("heart/spritesheet.png")
        # Definir el tamaño de cada fotograma de la sprite sheet
        self.width = self.spritesheet.get_width()/4
        self.height = self.spritesheet.get_height()
        # Diccionario de animaciones 
        self.frames = {
            "bomb": [(i * self.width, 0, self.width, self.height) for i in range(4)]  # 4 fotogramas para la animación 'bomb'
        } 
        self.animation_timer = 0  # Medir el tiempo para cambiar la animación
        self.frame_rate = 10  # Cada cuántos frames cambiamos la animación
        self.direction = 0  # Dirección (0: izquierda, 1: derecha)
        self.image = self.spritesheet.subsurface(self.frames["bomb"][0]) 
        self.vel_y = 0  # Reiniciar velocidad vertical
        #recurso sonido explosión
        self.platform = pygame.sprite.Group()
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("Explosion.wav")))
        self.sound.set_volume(0.5)
    #endregion
    
    #region set_Platform
    def set_Platform(self,platform):
        """
        Establece el grupo de plataformas con las que interactuará el Heart.

        Guarda el grupo de plataformas pasado como parámetro.

        :param platform: Grupo de plataformas (pygame.sprite.Group).
        :return: None
        """
        self.platform = platform
    #endregion
    
    #region active
    #funcion que lo activa para reutilización    
    def active(self,  x, y ,direction):
        """
        Activa el Heart, estableciendo posición, dirección y ajustando estado y parámetros.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param direction:  Dirección (0: izquierda, 1: derecha).
        :return: None
        """
        self.direction = direction
        super().active(x,y, direction)#posicion
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.index = 0
        super().set_use()#activación
        self.acc = 0.5
    #endregion
        
    #region animation
    #funcion que controla los cambios de la animación   
    def animation(self):
        """
        Gestiona la animación del Heart.

        Cambia el fotograma de la imagen, reproduce el sonido y hace que se deje de usar al finalizar la animación.

        :return: None
        """
        if self.index < len(self.frames["bomb"]):
            frame_rect = pygame.Rect(self.frames["bomb"][self.index])
            self.image = self.spritesheet.subsurface(frame_rect)
            self.index += 1
            if self.direction == 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_timer = 0
        else:
            self.sound.play
            super().set_use()
    #endregion
            
    #region stand_by
    def stand_by(self): 
        """
        Mueve el Heart fuera de la pantalla y detiene su movimiento.

        :return: None
        """
        self.rect.topleft = (-100, -100)  # La sacamos de la pantalla
        self.speed = 0
    #endregion
            
    #region update
    def update(self,):
        """
        Actualiza el estado del Heart en cada frame.

        Aplica gravedad, gestiona colisiones, y reproduce la animación.

        :return: None
        """
        if(self.inUse):
            self.animation_timer += 1
            self.vel_y += self.acc  # Aumenta la velocidad con la gravedad
            self.rect.y += self.vel_y  # Aplica la velocidad a la posición
            #manejo de collisiones 
            hits = pygame.sprite.spritecollide(self,self.platform, False)
            #if isInstace(hit, Breakable)>= self.frames[self.index]:
            #    hits.to_break() #desaparecera por lo tanto 
            if self.acc > 0:      
                for hit in hits:
                    if isinstance(hit, Platforms):
                        if self.rect.y + self.height > hit.rect.top:  # Si toca la plataforma
                            self.rect.y = hit.rect.top - self.height  # Ajustar posición
                            self.acc = 0  # Detener caída
                    if isinstance(hit, Breakable):
                        hit.on_bomb_Collision()  
            if self.animation_timer > self.frame_rate:
                self.animation()     
        else:
            self.stand_by()
    #endregion