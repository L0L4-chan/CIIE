'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''

import pygame , utils.auxiliar as auxiliar, utils.globals as globals    
from game.objects.oneuse import OneUse

class Fireball(OneUse):
     #region __init__
    def __init__(self):
        """
        Inicializa la clase Fireball.

        Carga la spritesheet, define dimensiones, frames de animación, sonido y otros atributos iniciales.
        """
        self.path = "fireball/spritesheet.png"
        super().__init__(self.path) 
        self.width = self.spritesheet.get_width()/7
        self.height = self.spritesheet.get_height()
        self.frames = {
            "bomb": [(i * self.width, 0, self.width, self.height) for i in range(7)]  # 7 fotogramas para la animación 'bomb'
        } 
        self.animation_timer = 0  # Medir el tiempo para cambiar la animación
        self.frame_rate = 120  # Cada cuántos frames cambiamos la animación
        self.direction = 1  # Dirección (-1: izquierda, 1: derecha)
        self.image = self.spritesheet.subsurface(self.frames["bomb"][0]) 
        self.vel_y = 0  # Reiniciar velocidad vertical
        #recurso sonido explosión
        self.sound = pygame.mixer.Sound(auxiliar.get_path(globals.config.get_audiofxpath("fire.wav")))
        self.sound.set_volume(0.5)
        self.counter = 3
    #endregion
    
    #region active
    def active(self, x, y ,direction ):
        """
        Activa la Fireball, estableciendo posición, dirección y aplicando ajustes visuales.

        :param x: Posición horizontal inicial.
        :param y: Posición vertical inicial.
        :param direction: Dirección en la que se moverá (1 para derecha, -1 para izquierda).
        :return: None
        """
        self.speed = 10 *  direction 
        super().active(x,y, direction)
        self.image = pygame.transform.scale(self.spritesheet, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.set_use()
    #endregion
        
    #region hit
    def hit(self):
        """
        Gestiona el impacto de la Fireball.

        Establece el estado de "no uso" para la Fireball. Si no está en uso, la mueve fuera de la pantalla.

        :return: None
        """
        self.set_use()  
        if not self.inUse:
            self.stand_by() 
    #endregion
     
    #region stand_by
    def stand_by(self): 
        """
        Mueve la fireball fuera de la pantalla y detiene su movimiento.

        :return: None
        """
        self.rect.topleft = (-100, -100)  # La sacamos de la pantalla
        self.speed = 0
    #endregion
        
    #region animation
    def animation(self):
        """
        Gestiona la animación de la Fireball.

        Cambia el frame de la imagen, reproduce el sonido y hace que se deje de usar al finalizar la animación.

        :return: None
        """
        if self.index < len(self.frames["bomb"]):
            frame_rect = pygame.Rect(self.frames["bomb"][self.index])
            self.image = self.spritesheet.subsurface(frame_rect)
            self.index += 1
            if self.direction <= 0:
                self.image = pygame.transform.flip(self.image, True, False)
            self.animation_timer = 0
        else:
            self.sound.play
            super().set_use()
    #endregion
    
    #region update
    def update(self, object = None):
        """
        Actualiza el estado de la Fireball en cada frame.

        Mueve la Fireball horizontalmente, gestiona el contador y la saca de la pantalla cuando es necesario.

        :param object: No utilizado, se mantiene por compatibilidad.
        :return: None
        """
        if(self.inUse):
            self.rect.y += self.speed
            self.counter -= 1
            if not self.on_screen and self.counter <= 0:
                self.inUse = False
                self.stand_by()
                self.counter = 3
    #endregion