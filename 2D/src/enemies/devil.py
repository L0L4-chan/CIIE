'''
Project: Skelly & Souli
Authors:

Ivan García Quintela
Ismael Míguez Valero
Lola Suárez González

Version: 1.0.0
'''
import pygame,   utils.globals as globals, utils.auxiliar as auxiliar
from classes.enemy import Enemy
from game.objects.stone import Stone


vec = pygame.math.Vector2  # 2 for two dimensional

class Devil(Enemy):
    
    def __init__(self, x, y):
        self.spritesheet = pygame.image.load(auxiliar.get_path(f"{ globals.config.get_artpath()}/devil/devil_spritesheet.png"))
        super().__init__(x,y, (self.spritesheet.get_width() /6), self.spritesheet.get_height(), False )
        
        self.vel = vec(globals.config.get_player_Acc()*2, 0)  # Velocidad inicial para moverse hacia la derecha
        self.speed = globals.config.get_player_Acc()
        self.frames = {
            "idle": [(0, 0)],
            "walk": [(i * self.width, 0) for i in range(4)],
            "death": [((self.width * 4 )+(i * self.width), 0) for i in range(2)]
        }
        self.can_shoot = 60
        self.projectiles = Stone()
        self.group.add(self.projectiles)
        self.lifes = 1
    
    #region move
    def move(self):
        """
        Gestiona el movimiento del diablo.

        Determina la dirección basada en la posición del objetivo, y se mueve horizontalmente y verticalmente.
        También gestiona el disparo si está cerca del objetivo.

        :return: None
        """
        self.set_objective()
        distance_x = self.objective[0] - self.rect.x
        distance_y = self.objective[1] - self.rect.y
        if distance_x < 0:
            self.direction = -1
        else:
            self.direction = 1
        if abs(distance_x) < self.screen_width/10:
            if abs(distance_y) < int(self.screen_width/20):
                self.check_bullets()
            else:
                self.vel.y = self.speed * (1 if distance_y > 0 else -1)
                self.pos.y += self.vel.y
        else:
            self.vel.x = self.speed * self.direction
            self.pos.x += self.vel.x
            
        self.update_rect()
    #endregion
            
    #region check_bullets
    def check_bullets(self):
        """
        Gestiona el contador de disparo y llama a la función shoot si es necesario.

        :return: None
        """
        self.can_shoot -=1
        if self.can_shoot < 0:
            self.shoot()
            self.can_shoot = 60      
    #endregion
          
    #region shoot
    def shoot(self):
        """
        Crea y dispara un proyectil (Stone).

        Calcula la posición del proyectil en función de la dirección del diablo, y activa el proyectil si no está en uso.

        :return: True si el proyectil se disparó, False en caso contrario.
        :rtype: bool
        """
        if self.direction > 0:
            stone_x = self.pos.x + (self.rect.width * self.direction)
        else:
            stone_x = self.pos.x - (self.rect.width)
        stone_y = self.rect.y + (self.height / 2)
        if self.projectiles.get_inUse():
            return False
        else:
            self.projectiles.active(x=stone_x, y=stone_y, direction = self.direction)
            return True
    #endregion